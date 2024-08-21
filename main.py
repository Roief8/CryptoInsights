from utils import generate_and_send_report

def main():
    try:
        generate_and_send_report()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()