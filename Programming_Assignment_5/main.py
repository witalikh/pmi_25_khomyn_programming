from Menu.interface_messages import prepare_messages
from Menu.queries import CertificatesQueriesThread


def main():
    menu_messages = prepare_messages()
    queries_thread_object = CertificatesQueriesThread("certificates.json", menu_messages)
    queries_thread_object.run_thread()


if __name__ == "__main__":
    main()
