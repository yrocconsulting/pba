<?php
/**
 * SEO and social sharing: meta description, Open Graph / Twitter cards,
 * WebSite + BreadcrumbList schema, sitemap and robots.txt tidy-up.
 *
 * Share image: the page's featured image if it has one, otherwise the
 * site-wide image in the pba_share_image setting (a Media Library ID).
 *
 * @package prestige-bass
 */

defined( 'ABSPATH' ) || exit;

add_action(
	'after_setup_theme',
	function () {
		add_theme_support( 'post-thumbnails' );
	}
);

add_action(
	'init',
	function () {
		add_post_type_support( 'page', 'excerpt' );
		register_setting(
			'general',
			'pba_share_image',
			array(
				'type'              => 'integer',
				'sanitize_callback' => 'absint',
				'show_in_rest'      => true,
				'default'           => 0,
			)
		);
	}
);

/**
 * Description for the current view (also used for social cards).
 */
function pba_meta_description() {
	if ( is_front_page() ) {
		return 'Guided bass fishing on Percy Priest Lake near Nashville, TN with live forward-facing sonar. Half day $550, full day $950 per boat for 1-2 anglers. $150 deposit secures your date.';
	}
	if ( is_singular() && has_excerpt() ) {
		return wp_strip_all_tags( get_the_excerpt() );
	}
	return get_bloginfo( 'description' );
}

/**
 * Share image for the current view: array( url, width, height, alt ) or null.
 */
function pba_share_image() {
	$id = 0;
	if ( is_singular() && has_post_thumbnail() ) {
		$id = get_post_thumbnail_id();
	}
	if ( ! $id ) {
		$id = (int) get_option( 'pba_share_image', 0 );
	}
	if ( ! $id ) {
		return null;
	}
	$src = wp_get_attachment_image_src( $id, 'full' );
	if ( ! $src ) {
		return null;
	}
	return array( $src[0], $src[1], $src[2], get_post_meta( $id, '_wp_attachment_image_alt', true ) );
}

add_action(
	'wp_head',
	function () {
		if ( is_admin() || is_feed() ) {
			return;
		}
		$site  = get_bloginfo( 'name' );
		$desc  = pba_meta_description();
		$url   = is_singular() ? get_permalink() : home_url( add_query_arg( array() ) );
		$title = is_front_page() ? $site . ' | Guided Bass Fishing on Percy Priest Lake, Nashville TN' : html_entity_decode( wp_strip_all_tags( get_the_title() ), ENT_QUOTES ) . ' | ' . $site;
		$img   = pba_share_image();

		$tags = array(
			array( 'name', 'description', $desc ),
			array( 'property', 'og:type', 'website' ),
			array( 'property', 'og:site_name', $site ),
			array( 'property', 'og:locale', 'en_US' ),
			array( 'property', 'og:title', $title ),
			array( 'property', 'og:description', $desc ),
			array( 'property', 'og:url', $url ),
			array( 'name', 'twitter:card', $img ? 'summary_large_image' : 'summary' ),
			array( 'name', 'twitter:title', $title ),
			array( 'name', 'twitter:description', $desc ),
		);
		if ( $img ) {
			$tags[] = array( 'property', 'og:image', $img[0] );
			$tags[] = array( 'property', 'og:image:secure_url', $img[0] );
			$tags[] = array( 'property', 'og:image:width', (string) $img[1] );
			$tags[] = array( 'property', 'og:image:height', (string) $img[2] );
			$tags[] = array( 'property', 'og:image:alt', $img[3] );
			$tags[] = array( 'name', 'twitter:image', $img[0] );
			$tags[] = array( 'name', 'twitter:image:alt', $img[3] );
		}
		foreach ( $tags as $t ) {
			if ( '' !== (string) $t[2] ) {
				printf( '<meta %s="%s" content="%s">' . "\n", $t[0], esc_attr( $t[1] ), esc_attr( $t[2] ) );
			}
		}

		// WebSite schema (site name for search results) on the home page.
		if ( is_front_page() ) {
			$data = array(
				'@context'  => 'https://schema.org',
				'@type'     => 'WebSite',
				'@id'       => home_url( '/#website' ),
				'name'      => $site,
				'url'       => home_url( '/' ),
				'publisher' => array( '@id' => home_url( '/#business' ) ),
			);
			echo '<script type="application/ld+json">' . wp_json_encode( $data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . "</script>\n";
		}

		// Breadcrumbs on inner pages: Home > Page.
		if ( is_page() && ! is_front_page() ) {
			$data = array(
				'@context'        => 'https://schema.org',
				'@type'           => 'BreadcrumbList',
				'itemListElement' => array(
					array( '@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => home_url( '/' ) ),
					array( '@type' => 'ListItem', 'position' => 2, 'name' => wp_strip_all_tags( get_the_title() ), 'item' => get_permalink() ),
				),
			);
			echo '<script type="application/ld+json">' . wp_json_encode( $data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . "</script>\n";
		}
	},
	2
);

// Sitemap: drop the users list (it exposes login names) and keep pages + posts.
add_filter(
	'wp_sitemaps_add_provider',
	function ( $provider, $name ) {
		return 'users' === $name ? false : $provider;
	},
	10,
	2
);
add_filter(
	'wp_sitemaps_taxonomies',
	function () {
		return array();
	}
);

// Author archives reveal login names and add nothing for visitors.
add_action(
	'template_redirect',
	function () {
		if ( is_author() || isset( $_GET['author'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification
			wp_safe_redirect( home_url( '/' ), 301 );
			exit;
		}
	},
	1 // Before WordPress's canonical redirect, which would reveal the login name.
);

// Point crawlers at the sitemap (applies when WordPress serves robots.txt).
add_filter(
	'robots_txt',
	function ( $output ) {
		if ( false === strpos( $output, 'Sitemap:' ) ) {
			$output .= "\nSitemap: " . home_url( '/wp-sitemap.xml' ) . "\n";
		}
		return $output;
	}
);

// Hide the public user list in the REST API (it exposes login names).
// Logged-in requests (WP Admin, the editor, Application Passwords) still work.
add_filter(
	'rest_endpoints',
	function ( $endpoints ) {
		if ( ! is_user_logged_in() ) {
			unset( $endpoints['/wp/v2/users'], $endpoints['/wp/v2/users/(?P<id>[\\d]+)'] );
		}
		return $endpoints;
	}
);
