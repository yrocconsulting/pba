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

		$towns = array( 'Nashville', 'Murfreesboro', 'Smyrna', 'La Vergne', 'Mt. Juliet', 'Hermitage', 'Antioch', 'Franklin', 'Brentwood', 'Nolensville', 'College Grove' );
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

		$offer = function ( $name, $desc, $price ) {
			return array(
				'@type'         => 'Offer',
				'name'          => $name,
				'description'   => $desc,
				'price'         => $price,
				'priceCurrency' => 'USD',
				'url'           => home_url( '/#book' ),
			);
		};

		$data = array(
			'@context'    => 'https://schema.org',
			'@type'       => array( 'LocalBusiness', 'SportsActivityLocation' ),
			'@id'         => home_url( '/#business' ),
			'name'        => 'Prestige Bass Adventures',
			'description' => 'Guided largemouth and smallmouth bass fishing trips on Percy Priest Lake near Nashville, Tennessee, with Captain Cory. Half-day and full-day trips priced per boat for 1 or 2 anglers; a 20% deposit secures the date. All skill levels welcome.',
			'url'         => home_url( '/' ),
			'telephone'   => '+1-615-310-1058',
			'priceRange'  => '$550–$950',
			'address'     => array(
				'@type'           => 'PostalAddress',
				'addressLocality' => 'College Grove',
				'addressRegion'   => 'TN',
				'postalCode'      => '37046',
				'addressCountry'  => 'US',
			),
			'areaServed'  => $area,
			'founder'     => array(
				'@type'    => 'Person',
				'name'     => 'Captain Cory',
				'jobTitle' => 'Owner and lead fishing guide',
			),
			'employee'    => array(
				array(
					'@type'    => 'Person',
					'name'     => 'Captain Cory',
					'jobTitle' => 'Fishing guide',
				),
				array(
					'@type'    => 'Person',
					'name'     => 'Captain John Boy',
					'jobTitle' => 'Fishing guide (large parties)',
				),
			),
			'makesOffer'  => array(
				$offer( 'Half-Day Guided Bass Fishing Trip', 'About 4 hours of guided bass fishing on Percy Priest Lake. Price is per boat for 1 or 2 anglers.', '550' ),
				$offer( 'Full-Day Guided Bass Fishing Trip', 'About 8 hours of guided bass fishing on Percy Priest Lake. Price is per boat for 1 or 2 anglers.', '950' ),
			),
		);

		$logo = get_site_icon_url( 512 );
		if ( $logo ) {
			$data['image'] = $logo;
		}

		echo '<script type="application/ld+json">' . wp_json_encode( $data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . "</script>\n";
	}
);
