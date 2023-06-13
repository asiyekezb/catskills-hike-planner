"""I need to hike a set of peaks. What are my options?

Sample invocation:

    poetry run python peak_planner.py H,BD,TC,C,Pl,Su,W,SW,KHP,Tw,IH,WHP
"""

import json

from subset_cover import find_optimal_hikes_subset_cover


PEAKS = [
    ('S', 2426171552, 'Slide Mountain'),
    ('H', 1938201532, 'Hunter Mountain'),
    ('BD', 2473476912, 'Blackdome Mountain'),
    ('BH', 2473476747, 'Blackhead Mountain'),
    ('TC', 2473476927, 'Thomas Cole Mountain'),
    ('We', 2955311547, 'West Kill Mountain'),
    ('C', 2884119551, 'Cornell Mountain'),
    ('Ta', 7292479776, 'Table Mountain'),
    ('Pk', 2398015279, 'Peekamoose Mountain'),
    ('Pl', 2882649917, 'Plateau Mountain'),
    ('Su', 2882649730, 'Sugarloaf Mountain'),
    ('W', 2884119672, 'Wittenberg Mountain'),
    ('SW', 1938215682, 'Southwest Hunter'),
    ('L', -1136, 'Lone Mountain'),
    ('BL', 2897919022, 'Balsam Lake Mountain'),
    ('P', 9147145385, 'Panther Mountain'),
    ('BI', 357548762, 'Big Indian Mtn Mountain'),
    ('Fr', 9953707705, 'Friday Mountain'),
    ('Ru', 10033501291, 'Rusk Mountain'),
    ('KHP', 9785950126, 'Kaaterskill High Peak'),
    ('Tw', 7982977638, 'Twin Mountain'),
    ('BC', 9953729846, 'Balsam Cap Mountain'),
    ('Fi', 357559622, 'Fir Mountain'),
    ('ND', 357574030, 'North Dome Mountain'),
    ('B', 2845338212, 'Balsam Mountain'),
    ('Bp', 212348771, 'Bearpen Mountain'),
    ('E', 357557378, 'Eagle Mountain'),
    ('IH', 7978185605, 'Indian Head Mountain'),
    ('Sh', 10010091368, 'Sherrill Mountain'),
    ('V', 10010051278, 'Vly Mountain'),
    ('WHP', 2426236522, 'Windham High Peak'),
    ('Ha', 357563196, 'Halcott Mountain'),
    ('Ro', -538, 'Rocky Mountain'),
]


def plan_hikes(peaks_to_hike: list[str]):
    features = json.load(open('data/network+parking.geojson'))['features']
    all_hikes: list[tuple[float, list[int]]] = json.load(open('data/hikes.json'))

    ha_code_to_osm_id = {ha_code: osm_id for ha_code, osm_id, _name in PEAKS}
    osm_ids = [ha_code_to_osm_id[ha_code] for ha_code in peaks_to_hike]
    print(osm_ids)

    osm_ids_set = set(osm_ids)
    relevant_hikes = [
        h for h in all_hikes if any(peak_id in osm_ids_set for peak_id in h[1])
    ]

    out = {
        'peaks_to_hike': peaks_to_hike,
        'osm_ids': osm_ids,
        'relevant_hikes': len(relevant_hikes),
    }

    print(f'Unrestricted hikes: {len(relevant_hikes)}')
    d_km, chosen, fc = find_optimal_hikes_subset_cover(
        features, relevant_hikes, osm_ids
    )
    out['unrestricted'] = {
        'd_km': d_km,
        'd_mi': d_km * 0.621371,
        'num_hikes': len(chosen),
        'hikes': chosen,
        'features': fc,
    }
    print(f'  {len(chosen)} hikes: {d_km:.2f} km = {d_km * 0.621371:.2f} mi')

    print()
    loop_hikes = [(d, nodes) for d, nodes in relevant_hikes if nodes[0] == nodes[-1]]
    print(f'Loop hikes: {len(loop_hikes)}')
    d_km, chosen, fc = find_optimal_hikes_subset_cover(features, loop_hikes, osm_ids)
    print(f'  {len(chosen)} hikes: {d_km:.2f} km = {d_km * 0.621371:.2f} mi')

    out['loops'] = {
        'd_km': d_km,
        'd_mi': d_km * 0.621371,
        'num_hikes': len(chosen),
        'hikes': chosen,
        'features': fc,
    }

    return out
