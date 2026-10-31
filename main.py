# main.py

import sys

from convert_xls import convert_xls_to_csv
from send_emails import send_emails


def main() -> None:
    send = "--send" in sys.argv
    convert_xls_to_csv()
    send_emails(send)


if __name__ == "__main__":
    main()
