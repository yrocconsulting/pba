<?php
/**
 * Opening screen (hook-set montage) shown once per visit.
 *
 * Off until pba_intro_portrait is set (Settings → General or REST). The
 * landscape version is used on wide screens; both are muted so they can
 * autoplay. The script builds the overlay, so search engines and visitors
 * without JavaScript just see the page.
 *
 * @package prestige-bass
 */

defined( 'ABSPATH' ) || exit;

add_action(
	'init',
	function () {
		foreach ( array( 'pba_intro_portrait', 'pba_intro_landscape', 'pba_intro_poster' ) as $key ) {
			register_setting(
				'general',
				$key,
				array(
					'type'              => 'string',
					'sanitize_callback' => 'esc_url_raw',
					'show_in_rest'      => true,
					'default'           => '',
				)
			);
		}
	}
);

add_action(
	'admin_init',
	function () {
		add_settings_field(
			'pba_intro_portrait',
			'Intro video (portrait MP4)',
			function () {
				printf( '<input type="url" class="regular-text" name="pba_intro_portrait" value="%s"><p class="description">Opening screen shown once per visit. Leave blank to turn the intro off.</p>', esc_attr( get_option( 'pba_intro_portrait', '' ) ) );
			},
			'general'
		);
		add_settings_field(
			'pba_intro_landscape',
			'Intro video (widescreen MP4)',
			function () {
				printf( '<input type="url" class="regular-text" name="pba_intro_landscape" value="%s">', esc_attr( get_option( 'pba_intro_landscape', '' ) ) );
			},
			'general'
		);
		add_settings_field(
			'pba_intro_poster',
			'Intro poster image',
			function () {
				printf( '<input type="url" class="regular-text" name="pba_intro_poster" value="%s">', esc_attr( get_option( 'pba_intro_poster', '' ) ) );
			},
			'general'
		);
	}
);

add_action(
	'wp_footer',
	function () {
		$portrait = get_option( 'pba_intro_portrait', '' );
		if ( ! $portrait || is_admin() ) {
			return;
		}
		$landscape = get_option( 'pba_intro_landscape', '' );
		printf(
			'<div id="pba-intro-data" hidden data-portrait="%s" data-landscape="%s" data-poster="%s" data-site="%s"></div>' . "\n",
			esc_url( $portrait ),
			esc_url( $landscape ? $landscape : $portrait ),
			esc_url( get_option( 'pba_intro_poster', '' ) ),
			esc_attr( get_bloginfo( 'name' ) )
		);
	}
);
