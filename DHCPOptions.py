class TimeOffset:
    """DHCP Option 2 [RFC 2232]"""

    in_str_offset = ""

    out_str_cisco = ""
    out_str_linux = ""
    out_str_windows = ""

    def __init__(self, str_user):
        self.in_str_offset = str_user
        self.convert(self.in_str_offset)

    def convert(self, str_offset):
        """Converts input string to hex list"""
        #
        # string -> int_dec -> int_hex -> list_hex_byte
        #
        int_dec = int(str_offset) * 3600
        int_hex = [hex(int_dec >> i & 0xFF) for i in (24, 16, 8, 0)]
        self.out_str_cisco = "".join([(".%s" % (x[2:]) if i and not i % 2 else x[2:]) for i, x in enumerate(int_hex)])
        self.out_str_linux = str(int_dec)
        self.out_str_windows = "0x" + "".join(["%s" % (x[2:]) for x in int_hex])

    def get_raw_cisco(self):
        """Returns conversion result for Cisco"""
        return self.out_str_cisco

    def get_raw_linux(self):
        """Returns conversion result for Linux"""
        return self.out_str_linux

    def get_raw_windows(self):
        """Returns conversion result for Windows"""
        return self.out_str_windows

    def get_human(self):
        """Prints human-readable conversion result"""
        print "\nTime Offset String: " + self.in_str_offset
        print "\nCisco DHCP (IOS):"
        print "option 2 hex " + self.get_raw_cisco()
        print "\nLinux DHCP (dhcpd.conf):"
        print "option time-offset " + self.get_raw_linux() + ";"
        print "\nWindows DHCP (PowerShell):"
        print "Set-DhcpServerV4OptionValue -OptionId 2 -Value " + self.get_raw_windows()
        print "\n---------------"

class DomainSearch:
    """DHCP Option 119 [RFC 3397]"""

    in_str_domain = ""
    in_str_len_max = 255

    out_str_cisco = ""
    out_str_linux = ""
    out_str_windows = ""

    def __init__(self, str_user):
        self.in_str_domain = str_user
        in_str_len = len(self.in_str_domain)
        if in_str_len == 0 or in_str_len > self.in_str_len_max:
            print "ERROR: Input string exceeded " + in_str_len_max + " chars"
            return
        else:
            self.convert(self.in_str_domain)

    def convert(self, str_domain):
        """Converts input string to hex list"""
        hex_data = []
        for fqdn in str_domain.split():
            for dc in fqdn.split("."):
                hex_data.extend(["0x%02x" % len(dc)] + ["0x" + smb.encode("hex") for smb in dc])
            hex_data.append("0x00")
        self.out_str_cisco = "".join([(".%s" % (x[2:]) if i and not i % 2 else x[2:]) for i, x in enumerate(hex_data)])
        self.out_str_linux = ", ".join('"{}"'.format(fqdn) for fqdn in str_domain.split())
        self.out_str_windows = ",".join(hex_data)

    def get_raw_cisco(self):
        """Returns conversion result for Cisco"""
        return self.out_str_cisco

    def get_raw_linux(self):
        """Returns conversion result for Linux"""
        return self.out_str_linux

    def get_raw_windows(self):
        """Returns conversion result for Windows"""
        return self.out_str_windows

    def get_human(self):
        """Prints human-readable conversion result"""
        print "\nDomain Search String: " + self.in_str_domain
        print "\nCisco DHCP (IOS):"
        print "option 119 hex " + self.get_raw_cisco()
        print "\nLinux DHCP (dhcpd.conf):"
        print "option domain-search " + self.get_raw_linux() + ";"
        print "\nWindows DHCP (PowerShell):"
        print "Set-DhcpServerV4OptionValue -OptionId 119 -Value " + self.get_raw_windows()
        print "\n---------------"
