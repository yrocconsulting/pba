<?php
/**
 * Background music with an always-visible on/off button.
 *
 * Off until a track is set: Settings → General → "Background music URL"
 * (or the pba_music_url setting via the REST API). Browsers only allow sound
 * after the visitor clicks or taps, so the script starts the music on the
 * first interaction unless the visitor has turned it off.
 *
 * @package prestige-bass
 */

defined( 'ABSPATH' ) || exit;

add_action(
	'init',
	function () {
		register_setting(
			'general',
			'pba_music_url',
			array(
				'type'              => 'string',
				'sanitize_callback' => 'esc_url_raw',
				'show_in_rest'      => true,
				'default'           => '',
			)
		);
		register_setting(
			'general',
			'pba_music_volume',
			array(
				'type'              => 'number',
				'sanitize_callback' => function ( $v ) {
					return max( 0.05, min( 1, (float) $v ) );
				},
				'show_in_rest'      => true,
				'default'           => 0.4,
			)
		);
	}
);

add_action(
	'admin_init',
	function () {
		add_settings_field(
			'pba_music_url',
			'Background music URL',
			function () {
				printf(
					'<input type="url" class="regular-text" name="pba_music_url" value="%s"><p class="description">MP3 from the Media Library. Leave blank to turn music off. Use only music you have the rights to.</p>',
					esc_attr( get_option( 'pba_music_url', '' ) )
				);
			},
			'general'
		);
	}
);

add_action(
	'wp_footer',
	function () {
		$src = get_option( 'pba_music_url', '' );
		if ( ! $src || is_admin() ) {
			return;
		}
		printf(
			'<button type="button" class="pba-music" data-src="%1$s" data-volume="%2$s" aria-pressed="false" aria-label="Play music" hidden>'
			. '<span class="pba-music__bars" aria-hidden="true"><i></i><i></i><i></i><i></i></span>'
			. '<span class="pba-music__label">Sound on</span></button>' . "\n",
			esc_url( $src ),
			esc_attr( (string) get_option( 'pba_music_volume', 0.4 ) )
		);
	}
);
