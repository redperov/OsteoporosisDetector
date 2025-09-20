import numpy as np
from tensorflow.keras.models import load_model
import tensorflow_hub as hub


class OsteoporosisPredictor:
    def __init__(self, model_path):
        self.model = self._load_model(model_path)

    def predict(self, image, image_name):
        y_probs = self.model.predict(np.array([image]))
        y_pred = np.argmax(y_probs[0])
        y_prob = y_probs[0][y_pred]
        print(f"Classification for image: {image_name} is: {y_pred} with probability: {y_prob}")
        return y_pred, y_prob

    @staticmethod
    def _load_model(model_path):
        import tensorflow as tf
        from tensorflow import keras
        import tensorflow_hub as hub
        
        try:
            # First approach: Use custom_object_scope (recommended by TensorFlow)
            print("Attempting to load model with custom_object_scope...")
            with keras.utils.custom_object_scope({'KerasLayer': hub.KerasLayer}):
                model = load_model(model_path)
            print("Model loaded successfully with custom_object_scope")
            return model
        except Exception as e1:
            print(f"Failed to load with custom_object_scope: {e1}")
            
            try:
                # Second approach: Use custom_object_scope with compile=False
                print("Attempting to load with custom_object_scope and compile=False...")
                with keras.utils.custom_object_scope({'KerasLayer': hub.KerasLayer}):
                    model = load_model(model_path, compile=False)
                print("Model loaded successfully with custom_object_scope and no compilation")
                return model
            except Exception as e2:
                print(f"Failed to load with custom_object_scope and compile=False: {e2}")
                
                try:
                    # Third approach: Direct custom_objects parameter
                    print("Attempting to load with direct custom_objects...")
                    model = load_model(model_path, 
                                     custom_objects={'KerasLayer': hub.KerasLayer},
                                     compile=False)
                    print("Model loaded successfully with direct custom_objects")
                    return model
                except Exception as e3:
                    print(f"Failed to load with direct custom_objects: {e3}")
                    
                    try:
                        # Fourth approach: Try loading weights only
                        print("Attempting to recreate model architecture and load weights...")
                        # This would require knowing the original model architecture
                        # For now, we'll skip this and raise an error
                        raise Exception("Model architecture recreation not implemented")
                    except Exception as e4:
                        print(f"All loading attempts failed. Last error: {e4}")
                        raise RuntimeError(f"Could not load model from {model_path}. "
                                         f"This model may have been saved with an incompatible version of TensorFlow/TensorFlow Hub. "
                                         f"Consider re-training the model with the current environment.")
