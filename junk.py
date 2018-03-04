#!/usr/bin/env python



clients_integrations = {8053450:['google_analytics', 'twitter', 'facebook','instagram'],
                        226:['facebook','instagram','twitter','google_analytics','weather','presence'],
                        64068610:['facebook','instagram','twitter','google_analytics'],
                        246:['facebook','twitter'],
                        56796913:['facebook','instagram','twitter','google_analytics'],
                        64068615:['facebook','instagram','twitter','google_analytics','weather','presence'],
                        4923512:['facebook','twitter','google_analytics','weather'],
                        7288062:['facebook','twitter','google_analytics'],
                        7855164:['facebook','twitter','google_analytics','weather','presence']
                        }


venue_integrations = clients_integrations[8053450]
print(venue_integrations)
for i in venue_integrations:
    print(i)