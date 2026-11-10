<?php
/**
 * Prestige Bass Adventures theme functions.
 *
 * @package prestige-bass
 */

defined( 'ABSPATH' ) || exit;

define( 'PBA_VERSION', '1.3.1' );
define( 'PBA_DIR', get_template_directory() );
define( 'PBA_URI', get_template_directory_uri() );

require PBA_DIR . '/inc/booking-form.php';
require PBA_DIR . '/inc/schema.php';
require PBA_DIR . '/inc/deploy.php';

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

// Strip emoji scripts; the site doesn't need them.
remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );
