<?php
/**
 * Booking request form: [pba_booking_form] shortcode.
 *
 * Every request is saved as a private "Trip Request" in WP Admin, so nothing is
 * lost if email delivery fails, and an email notification is sent to the
 * address in Settings → General → "Booking notification email".
 *
 * @package prestige-bass
 */

defined( 'ABSPATH' ) || exit;

/**
 * Lakes offered in the form's dropdown. Filterable so the list can change
 * without editing the form.
 */
function pba_lakes() {
	return apply_filters(
		'pba_lakes',
		array( 'Percy Priest Lake' )
	);
}

add_action(
	'init',
	function () {
		register_post_type(
			'pba_inquiry',
			array(
				'labels'          => array(
					'name'          => 'Trip Requests',
					'singular_name' => 'Trip Request',
					'menu_name'     => 'Trip Requests',
					'all_items'     => 'All Trip Requests',
				),
				'public'          => false,
				'show_ui'         => true,
				'show_in_menu'    => true,
				'show_in_rest'    => false,
				'menu_icon'       => 'dashicons-calendar-alt',
				'menu_position'   => 3,
				'supports'        => array( 'title', 'editor' ),
				'capability_type' => 'post',
				'capabilities'    => array( 'create_posts' => 'do_not_allow' ),
				'map_meta_cap'    => true,
			)
		);

		register_setting(
			'general',
			'pba_booking_email',
			array(
				'type'              => 'string',
				'sanitize_callback' => 'sanitize_email',
				'show_in_rest'      => true,
				'default'           => '',
			)
		);

		add_shortcode( 'pba_booking_form', 'pba_render_booking_form' );
	}
);

add_action(
	'admin_init',
	function () {
		add_settings_field(
			'pba_booking_email',
			'Booking notification email',
			function () {
				printf(
					'<input type="email" class="regular-text" name="pba_booking_email" value="%s"><p class="description">Trip requests from the website are emailed here. Leave blank to use the site admin email.</p>',
					esc_attr( get_option( 'pba_booking_email', '' ) )
				);
			},
			'general'
		);
	}
);

/**
 * Render the form.
 */
function pba_render_booking_form() {
	$status = isset( $_GET['booking'] ) ? sanitize_key( wp_unslash( $_GET['booking'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification

	ob_start();
	if ( 'sent' === $status ) {
		echo '<div class="pba-form__notice pba-form__notice--ok" role="status"><strong>Request received.</strong> We&rsquo;ll call or text you shortly to lock in your date.</div>';
	} elseif ( 'error' === $status ) {
		echo '<div class="pba-form__notice pba-form__notice--err" role="alert">Something went wrong. Please fill in your name and a phone number or email, or just call <a href="tel:+16153101058">(615) 310-1058</a>.</div>';
	}
	?>
	<form class="pba-form" method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
		<input type="hidden" name="action" value="pba_booking">
		<?php wp_nonce_field( 'pba_booking', 'pba_nonce' ); ?>
		<div class="pba-form__hp" aria-hidden="true"><label>Leave this empty <input type="text" name="pba_website" tabindex="-1" autocomplete="off"></label></div>

		<fieldset class="pba-form__trip">
			<legend>Choose your trip</legend>
			<label class="pba-radio"><input type="radio" name="trip" value="Half Day" checked><span><b>Half Day</b><small>$550 &middot; ~4 hours on the water</small></span></label>
			<label class="pba-radio"><input type="radio" name="trip" value="Full Day"><span><b>Full Day</b><small>$950 &middot; ~8 hours on the water</small></span></label>
		</fieldset>

		<div class="pba-form__row">
			<label>Name<input type="text" name="name" required autocomplete="name"></label>
			<label>Phone<input type="tel" name="phone" autocomplete="tel"></label>
		</div>
		<div class="pba-form__row">
			<label>Email<input type="email" name="email" autocomplete="email"></label>
			<label>Preferred date<input type="date" name="date"></label>
		</div>
		<?php $pba_lakes = pba_lakes(); ?>
		<div class="pba-form__row">
			<label>Party size <span class="pba-form__opt">(2 per boat)</span>
				<select name="anglers"><option>1</option><option selected>2</option><option>3</option><option>4</option><option>5</option><option>6+</option></select>
			</label>
			<?php if ( count( $pba_lakes ) > 1 ) : ?>
			<label>Lake
				<select name="lake">
					<option value="">Captain's choice</option>
					<?php foreach ( $pba_lakes as $lake ) : ?>
						<option><?php echo esc_html( $lake ); ?></option>
					<?php endforeach; ?>
				</select>
			</label>
			<?php else : ?>
			<input type="hidden" name="lake" value="<?php echo esc_attr( $pba_lakes[0] ); ?>">
			<?php endif; ?>
			<label>Start time
				<select name="start"><option>Either</option><option>Morning</option><option>Afternoon</option></select>
			</label>
		</div>
		<label>Anything else? <span class="pba-form__opt">(experience level, kids along, what you want to catch, large-party details)</span>
			<textarea name="message" rows="4"></textarea>
		</label>
		<button type="submit" class="wp-element-button pba-btn">Request my trip</button>
		<p class="pba-form__fine">No payment now. Once we confirm your date, a 20% deposit secures it. $550 / $950 per boat, 1&ndash;2 anglers.</p>
	</form>
	<?php
	return ob_get_clean();
}

/**
 * Handle submissions.
 */
function pba_handle_booking() {
	$back = wp_get_referer() ? wp_get_referer() : home_url( '/' );
	$back = remove_query_arg( 'booking', $back );
	$back = strtok( $back, '#' );

	$fail = function () use ( $back ) {
		wp_safe_redirect( add_query_arg( 'booking', 'error', $back ) . '#book' );
		exit;
	};

	if ( ! isset( $_POST['pba_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['pba_nonce'] ) ), 'pba_booking' ) ) {
		$fail();
	}

	// Honeypot: bots fill every field. Pretend success.
	if ( ! empty( $_POST['pba_website'] ) ) {
		wp_safe_redirect( add_query_arg( 'booking', 'sent', $back ) . '#book' );
		exit;
	}

	// Basic rate limit: 5 requests per IP per hour.
	$ip  = isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : 'unknown';
	$key = 'pba_rl_' . md5( $ip );
	$hit = (int) get_transient( $key );
	if ( $hit >= 5 ) {
		$fail();
	}
	set_transient( $key, $hit + 1, HOUR_IN_SECONDS );

	$f = array();
	foreach ( array( 'trip', 'name', 'phone', 'email', 'date', 'anglers', 'lake', 'start' ) as $k ) {
		$f[ $k ] = isset( $_POST[ $k ] ) ? sanitize_text_field( wp_unslash( $_POST[ $k ] ) ) : '';
	}
	$f['email']   = sanitize_email( $f['email'] );
	$f['message'] = isset( $_POST['message'] ) ? sanitize_textarea_field( wp_unslash( $_POST['message'] ) ) : '';

	if ( '' === $f['name'] || ( '' === $f['phone'] && '' === $f['email'] ) ) {
		$fail();
	}

	$lines = array(
		'Trip: ' . $f['trip'],
		'Name: ' . $f['name'],
		'Phone: ' . $f['phone'],
		'Email: ' . $f['email'],
		'Preferred date: ' . $f['date'],
		'Party size: ' . $f['anglers'],
		'Start time: ' . ( $f['start'] ? $f['start'] : 'Either' ),
		'Lake: ' . ( $f['lake'] ? $f['lake'] : "Captain's choice" ),
		'',
		$f['message'],
	);
	if ( in_array( $f['anglers'], array( '3', '4', '5', '6+' ), true ) ) {
		array_unshift( $lines, 'LARGE PARTY: more than 2 anglers, plan a second boat (Captain John Boy).', '' );
	}
	$body = implode( "\n", $lines );

	wp_insert_post(
		array(
			'post_type'    => 'pba_inquiry',
			'post_status'  => 'private',
			'post_title'   => sprintf( '%s · %s · %s', $f['name'], $f['trip'], $f['date'] ? $f['date'] : 'date TBD' ),
			'post_content' => $body,
		)
	);

	$to      = get_option( 'pba_booking_email' );
	$to      = is_email( $to ) ? $to : get_option( 'admin_email' );
	$headers = array();
	if ( is_email( $f['email'] ) ) {
		$headers[] = 'Reply-To: ' . $f['name'] . ' <' . $f['email'] . '>';
	}
	wp_mail( $to, 'New trip request: ' . $f['name'] . ' (' . $f['trip'] . ')', $body, $headers );

	wp_safe_redirect( add_query_arg( 'booking', 'sent', $back ) . '#book' );
	exit;
}
add_action( 'admin_post_nopriv_pba_booking', 'pba_handle_booking' );
add_action( 'admin_post_pba_booking', 'pba_handle_booking' );
