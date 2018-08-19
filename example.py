import DHCPOptions

opt2 = DHCPOptions.TimeOffset("3")
opt2.get_human()

opt119 = DHCPOptions.DomainSearch("example.com corp.example.com")
opt119.get_human()
