# Static route
    configure
    set groups template1 policy-options policy-statement from_static term 1 from protocol static
    set groups template1 policy-options policy-statement from_static term 1 then accept
    set groups template1 routing-options static route 0.0.0.0/0 next-hop 10.100.2.254
    set groups template1 protocols isis export from_static
    set apply-groups template1
    commit

# point-to-point isis

    configure
    {% if interfaces and interfaces | length > 0 %}
    {% for interface in interfaces %}
    set groups template2 protocols isis interface {{interface}} point-to-point
    set groups template2 protocols isis interface {{interface}} delay-measurement 
    {% endfor %}
    {% endif %}
    set groups template2 services rpm twamp server authentication-mode none 
    set groups template2 services rpm twamp server light 
    set apply-groups template2
    commit

# bgp-LS


    configure
    set group2 template3 routing-options autonomous-system {{ASN}}
    set group2 template3 protocols bgp group to_pa2 type internal
    set group2 template3 protocols bgp group to_pa2 description "Paragon BGP-TE Peering"
    set group2 template3 protocols bgp group to_pa2 family traffic-engineering unicast
    set groups template3 protocols bgp group to_pa2 allow 0.0.0.0/0
    set groups template3 protocols bgp group to_pa2 export TE
    set groups template3 protocols bgp group to_pa2 local-address {{local_address}}
    set groups template3 policy-options policy-statement TE term 1 from family traffic-engineering 
    set groups template3 policy-options policy-statement TE term 1 accept
    set groups template3 protocols mpls traffic-engineering database import policy TE
    set apply-groups template3
    commit

