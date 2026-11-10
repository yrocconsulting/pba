<?php
/**
 * Structured data (JSON-LD) so search engines and AI assistants understand
 * the business: who, what, where, and how to book.
 *
 * @package prestige-bass
 */

defined( 'ABSPATH' ) || exit;

add_action(
	'wp_head',
	function () {
		if ( ! is_front_page() ) {
			return;
		}

		$towns = array( 'Nashville', 'Franklin', 'Brentwood', 'Murfreesboro', 'Spring Hill', 'Nolensville', 'Smyrna', 'Columbia', 'College Grove' );
		$area  = array();
		foreach ( $towns as $t ) {
			$area[] = array(
				'@type' => 'City',
				'name'  => $t . ', TN',
			);
		}
		foreach ( pba_lakes() as $lake ) {
			$area[] = array(
				'@type' => 'LakeBodyOfWater',
				'name'  => $lake,
			);
		}

		$offer = function ( $name, $desc ) {
			return array(
				'@type'       => 'Offer',
				'name'        => $name,
				'description' => $desc,
				'url'         => home_url( '/#book' ),
			);
		};

		$data = array(
			'@context'    => 'https://schema.org',
			'@type'       => array( 'LocalBusiness', 'SportsActivityLocation' ),
			'@id'         => home_url( '/#business' ),
			'name'        => 'Prestige Bass Adventures',
			'description' => 'Guided largemouth and smallmouth bass fishing trips on Middle Tennessee lakes with Captain Cory Anderson. Half-day and full-day trips; all skill levels.',
			'url'         => home_url( '/' ),
			'telephone'   => '+1-615-310-1058',
			'priceRange'  => '$$',
			'address'     => array(
				'@type'           => 'PostalAddress',
				'addressLocality' => 'College Grove',
				'addressRegion'   => 'TN',
				'postalCode'      => '37046',
				'addressCountry'  => 'US',
			),
			'areaServed'  => $area,
			'founder'     => array(
				'@type' => 'Person',
				'name'  => 'Cory Anderson',
			),
			'makesOffer'  => array(
				$offer( 'Half-Day Guided Bass Fishing Trip', 'About 4 hours of guided bass fishing.' ),
				$offer( 'Full-Day Guided Bass Fishing Trip', 'About 8 hours of guided bass fishing.' ),
			),
		);

		$logo = get_site_icon_url( 512 );
		if ( $logo ) {
			$data['image'] = $logo;
		}

		echo '<script type="application/ld+json">' . wp_json_encode( $data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . "</script>\n";
	}
);
