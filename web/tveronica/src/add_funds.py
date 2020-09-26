from search import KeyClient
from main import FUND_PREFIX

client = KeyClient()

with open("/opt/scripts/funds.txt") as f:
    funds = f.readlines()

if __name__ == "__main__":
    def add_fund(name, val):
        client.write_prefix(
            FUND_PREFIX,
            name,
            val
        )

    for fund in funds:
        name, val = fund.split(":")
        add_fund(name, val)
    print(f'[+] Created {len(funds)} funds.')

