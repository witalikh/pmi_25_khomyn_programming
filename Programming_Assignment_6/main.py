from menu import CertificatesQueriesThread, prepare_messages


def main():
    menu_messages = prepare_messages("lang_uk.json")
    queries_thread_object = CertificatesQueriesThread("certificates.json", menu_messages)
    queries_thread_object.run_thread()


if __name__ == "__main__":
    main()
