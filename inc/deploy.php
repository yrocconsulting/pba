<?php
/**
 * Theme self-deploy endpoint (enabled at the site owner's request).
 *
 * POST /wp-json/pba/v1/deploy   body: the theme .zip (Content-Type: application/zip)
 * GET  /wp-json/pba/v1/deploy   returns the installed theme version
 *
 * Restricted to users who can install AND update themes (administrators),
 * authenticated with an Application Password. It does the same thing as
 * Appearance → Themes → Upload Theme → "Replace active with uploaded", and
 * only accepts a zip of this theme (prestige-bass/style.css must be inside).
 *
 * To turn it off, define PBA_DISABLE_DEPLOY as true in wp-config.php or
 * remove this file.
 *
 * @package prestige-bass
 */

defined( 'ABSPATH' ) || exit;

if ( defined( 'PBA_DISABLE_DEPLOY' ) && PBA_DISABLE_DEPLOY ) {
	return;
}

add_action(
	'rest_api_init',
	function () {
		$can = function () {
			return current_user_can( 'install_themes' ) && current_user_can( 'update_themes' );
		};

		register_rest_route(
			'pba/v1',
			'/deploy',
			array(
				array(
					'methods'             => 'GET',
					'permission_callback' => $can,
					'callback'            => function () {
						return array( 'version' => wp_get_theme( 'prestige-bass' )->get( 'Version' ) );
					},
				),
				array(
					'methods'             => 'POST',
					'permission_callback' => $can,
					'callback'            => 'pba_deploy_theme',
				),
			)
		);
	}
);

/**
 * Install the uploaded zip over the current theme.
 *
 * @param WP_REST_Request $request Request whose body is the zip.
 * @return array|WP_Error
 */
function pba_deploy_theme( WP_REST_Request $request ) {
	if ( defined( 'DISALLOW_FILE_MODS' ) && DISALLOW_FILE_MODS ) {
		return new WP_Error( 'pba_file_mods', 'File changes are disabled on this site.', array( 'status' => 403 ) );
	}

	$body = $request->get_body();
	if ( strlen( $body ) < 100 || strlen( $body ) > 30 * MB_IN_BYTES || 0 !== strpos( $body, "PK\x03\x04" ) ) {
		return new WP_Error( 'pba_bad_zip', 'Body must be a theme zip under 30 MB.', array( 'status' => 400 ) );
	}

	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/misc.php';
	require_once ABSPATH . 'wp-admin/includes/theme.php';
	require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';

	$tmp = wp_tempnam( 'prestige-bass.zip' );
	file_put_contents( $tmp, $body ); // phpcs:ignore WordPress.WP.AlternativeFunctions

	// The archive must be this theme and nothing else.
	if ( class_exists( 'ZipArchive' ) ) {
		$zip = new ZipArchive();
		$ok  = ( true === $zip->open( $tmp ) );
		if ( $ok ) {
			$ok = false !== $zip->locateName( 'prestige-bass/style.css' );
			for ( $i = 0; $ok && $i < $zip->numFiles; $i++ ) {
				$name = $zip->getNameIndex( $i );
				if ( 0 !== strpos( $name, 'prestige-bass/' ) || false !== strpos( $name, '..' ) ) {
					$ok = false;
				}
			}
			$zip->close();
		}
		if ( ! $ok ) {
			wp_delete_file( $tmp );
			return new WP_Error( 'pba_wrong_theme', 'Zip must contain only the prestige-bass theme folder.', array( 'status' => 400 ) );
		}
	}

	if ( ! WP_Filesystem() ) {
		wp_delete_file( $tmp );
		return new WP_Error( 'pba_fs', 'WordPress could not get direct file access.', array( 'status' => 500 ) );
	}

	$before   = wp_get_theme( 'prestige-bass' )->get( 'Version' );
	$skin     = new WP_Ajax_Upgrader_Skin();
	$upgrader = new Theme_Upgrader( $skin );
	$result   = $upgrader->install( $tmp, array( 'overwrite_package' => true ) );
	wp_delete_file( $tmp );

	if ( is_wp_error( $result ) ) {
		return $result;
	}
	if ( ! $result ) {
		$errors = $skin->get_errors();
		return new WP_Error( 'pba_install_failed', $errors->has_errors() ? $errors->get_error_message() : 'Install failed.', array( 'status' => 500 ) );
	}

	wp_clean_themes_cache();
	clearstatcache();
	$after = get_file_data( get_theme_root( 'prestige-bass' ) . '/prestige-bass/style.css', array( 'Version' => 'Version' ) );

	return array(
		'deployed' => true,
		'from'     => $before,
		'to'       => $after['Version'],
	);
}
