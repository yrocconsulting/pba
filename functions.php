<?php
/**
 * Prestige Bass Adventures theme functions.
 *
 * @package prestige-bass
 */

defined( 'ABSPATH' ) || exit;

define( 'PBA_VERSION', '1.7.0' );
define( 'PBA_DIR', get_template_directory() );
define( 'PBA_URI', get_template_directory_uri() );

require PBA_DIR . '/inc/booking-form.php';
require PBA_DIR . '/inc/schema.php';
require PBA_DIR . '/inc/deploy.php';
require PBA_DIR . '/inc/music.php';

add_action(
	'after_setup_theme',
	function () {
		add_theme_support( 'wp-block-styles' );
		add_theme_support( 'editor-styles' );
		add_theme_support( 'responsive-embeds' );
		add_editor_style( 'assets/css/main.css' );
	}
);

add_action(
	'wp_enqueue_scripts',
	function () {
		$css = PBA_DIR . '/assets/css/main.css';
		$js  = PBA_DIR . '/assets/js/main.js';
		wp_enqueue_style( 'pba-main', PBA_URI . '/assets/css/main.css', array(), PBA_VERSION . '.' . filemtime( $css ) );
		wp_enqueue_script( 'pba-main', PBA_URI . '/assets/js/main.js', array(), PBA_VERSION . '.' . filemtime( $js ), array( 'strategy' => 'defer', 'in_footer' => true ) );
	}
);

// Preload the display font so the hero headline doesn't flash.
add_action(
	'wp_head',
	function () {
		printf(
			'<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' . "\n",
			esc_url( PBA_URI . '/assets/fonts/big-shoulders-display.woff2' )
		);
		echo '<meta name="theme-color" content="#070707">' . "\n";
	},
	1
);

// Pages get excerpts; they double as the meta description.
add_action( 'init', function () { add_post_type_support( 'page', 'excerpt' ); } );

add_action(
	'wp_head',
	function () {
		$desc = '';
		if ( is_front_page() ) {
			$desc = 'Guided bass fishing on Percy Priest Lake near Nashville, TN. Live forward-facing sonar. Half day $550, full day $950 per boat for 1-2 anglers.';
		} elseif ( is_singular() && has_excerpt() ) {
			$desc = get_the_excerpt();
		}
		if ( $desc ) {
			printf( '<meta name="description" content="%s">' . "\n", esc_attr( wp_strip_all_tags( $desc ) ) );
		}
	},
	2
);

// Strip emoji scripts; the site doesn't need them.
remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );
