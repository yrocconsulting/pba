<?php
/**
 * Structured data (JSON-LD) so search engines and AI assistants understand
 * the business: who, what, where, and how to book.
 *
 * @package prestige-bass
 */

defined( 'ABSPATH' ) || exit;

/**
 * FAQPage markup for the FAQ page, read from its Details blocks so it always
 * matches what's on the page.
 */
add_action(
	'wp_head',
	function () {
		if ( ! is_page( 'faq' ) ) {
			return;
		}
		$items = array();
		$walk  = function ( $blocks ) use ( &$walk, &$items ) {
			foreach ( $blocks as $b ) {
				if ( 'core/details' === $b['blockName'] && preg_match( '#<summary>(.*?)</summary>#s', $b['innerHTML'], $m ) ) {
					$answer = '';
					foreach ( $b['innerBlocks'] as $ib ) {
						$answer .= ' ' . wp_strip_all_tags( $ib['innerHTML'] );
					}
					$items[] = array(
						'@type'          => 'Question',
						'name'           => html_entity_decode( wp_strip_all_tags( $m[1] ), ENT_QUOTES ),
						'acceptedAnswer' => array(
							'@type' => 'Answer',
							'text'  => html_entity_decode( trim( preg_replace( '/\s+/', ' ', $answer ) ), ENT_QUOTES ),
						),
					);
				}
				if ( ! empty( $b['innerBlocks'] ) ) {
					$walk( $b['innerBlocks'] );
				}
			}
		};
		$walk( parse_blocks( get_post_field( 'post_content', get_queried_object_id() ) ) );
		if ( $items ) {
			echo '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => $items ), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . "</script>\n";
		}
	}
);

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
			'name'        => 'Premier Bass Adventures',
			'description' => 'Guided largemouth and smallmouth bass fishing trips on Percy Priest Lake near Nashville, Tennessee. Largemouth, smallmouth and spotted bass, plus the occasional striped bass. Half-day and full-day trips priced per boat for 1 or 2 anglers; a $150 deposit secures the date. All skill levels welcome.',
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
			$data['logo'] = $logo;
		}
		$share = function_exists( 'pba_share_image' ) ? pba_share_image() : null;
		if ( $share ) {
			$data['image'] = $share[0];
		} elseif ( $logo ) {
			$data['image'] = $logo;
		}

		echo '<script type="application/ld+json">' . wp_json_encode( $data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . "</script>\n";
	}
);
