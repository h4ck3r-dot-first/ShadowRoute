ShadowRoute: Automated Anonymity Toolkit for Kali Linux Using Tor & Proxychains

ShadowRoute is an automated anonymity framework designed to help ethical hackers and privacy-conscious users route all tool traffic through Tor and Proxychains with zero manual setup. Built for Kali Linux, this tool simplifies the complex, error-prone process of configuring anonymity layers — so you can focus on secure, stealthy operations.
Why ShadowRoute?

On the internet, your IP address is your identity. During reconnaissance, penetration testing, or OSINT activities, exposing your real IP can compromise your mission or put you at legal risk. ShadowRoute uses Tor and Proxychains to anonymize your internet traffic, masking your location and reducing traceability.
What It Does (Automatically):

    Installs and configures Tor.

    Installs Proxychains4 (if not present).

    Edits the proxychains4.conf file to:

        Enable dynamic_chain for flexible proxy routing.

        Enable proxy_dns to avoid DNS leaks.

        Set Tor’s SOCKS5 proxy (127.0.0.1:9050) as the default route.

    Starts and enables the Tor service on boot.

    Provides simple commands to:

        Run apps/tools through Tor.

        Check current IP anonymously.

        Restart Tor for a new identity (IP).

    Includes optional IP rotation with custom intervals.

Example Usage:

# Launch Firefox anonymously
shadowroute run firefox

# Get your Tor IP address
shadowroute ip

# Restart Tor for a new identity
shadowroute restart

Disclaimer:

ShadowRoute is for legal, ethical use only — such as penetration testing with permission, anonymous browsing, or privacy research. Misuse for illegal purposes is strictly prohibited and may result in legal consequences.
In Summary:

ShadowRoute turns a technical setup into a one-command tool. Whether you're a red teamer, cybersecurity student, or privacy advocate, ShadowRoute gets your Kali tools Tor-ready — fast, reliably, and safely.
