# Demo for doing ip address math.
# Demonstrates subtracting networks from a given list of networks.

import ipaddress

def find_all_available_networks(child_ip_network_list, parent_ip_network_list):
    # for each ip network in the list
    for child_ip_network in child_ip_network_list:
        # find the child ip network in the parent network list.
        for parent_ip_network in parent_ip_network_list:
            # Test to see if the parent network contains the child network.
            if child_ip_network.subnet_of(parent_ip_network):
                # remove from the parent network list
                remainder_networks_of_parent_network = list(parent_ip_network.address_exclude(child_ip_network))
                # remove the original parent network from the original list
                parent_ip_network_list.remove(parent_ip_network)
                # add the new available parent networks to the parent networks list being the result of subtracting the child network.
                parent_ip_network_list = parent_ip_network_list + remainder_networks_of_parent_network
    return parent_ip_network_list  # return the available networks


def find_next_available_network(parent_ip_network_list, desired_cidr_mask):
    # sort our list by prefix length
    parent_ip_network_list = sorted(parent_ip_network_list, key=lambda x: x.prefixlen, reverse=True)
    # find the smallest network that could contain our desired network size.
    for parent_ip_network in parent_ip_network_list:
        if desired_cidr_mask >= parent_ip_network.prefixlen:
            # if we found one exactly the right size then return that as the new network.
            if desired_cidr_mask == parent_ip_network.prefixlen:
                return parent_ip_network.exploded
            else:
                # if it is not exactly the right size, return the new network.
                return f"{parent_ip_network.network_address}/{desired_cidr_mask}"


if __name__ == '__main__':
    parent_network = ipaddress.ip_network('10.0.1.0/24')  # parent block for a region
    n2 = ipaddress.ip_network('10.0.1.0/29')  # ips for a vnet.
    n3 = ipaddress.ip_network('10.0.1.8/29')  # ips for a vnet.
    n4 = ipaddress.ip_network('10.0.1.16/29')  # ips for a vnet.
    # get the remaining networks
    remaining = find_all_available_networks([n2, n3, n4], [parent_network])
    print(remaining)
    # get the next available network of a size.
    print("looking for a new network of size 28")
    print(find_next_available_network(remaining, 28))
