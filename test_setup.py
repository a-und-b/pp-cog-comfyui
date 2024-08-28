from predict import Predictor

def test_setup():
    try:
        predictor = Predictor()
        predictor.setup()
        print("Setup completed successfully!")
    except Exception as e:
        print(f"Error during setup: {str(e)}")

if __name__ == "__main__":
    test_setup()