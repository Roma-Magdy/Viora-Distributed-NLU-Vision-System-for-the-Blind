##  1. Viora NLU Server (Port 8000)
This server is the brain that converts user speech/text into system actions. Use this guide to connect your backend service to the NLU engine.

### Connection Details
* **Base URL:** `https://8000-01kp795e7c121r8a8jj0d78qwt.cloudspaces.litng.ai`
* **Endpoint:** `/api/v1/parse`
* **Protocol:** `HTTP POST (JSON)`

### Request Structure
Your app must send a JSON body with the following format:

| Key | Type | Description |
| :--- | :--- | :--- |
| **`text`** | `string` | The user's voice command or typed message (Arabic/English). |

### Output Fields
* **`viora_reply`**: The actual string to speak or display (Egyptian Arabic).
* **`decision`**: The system code that tells your app what to do next (e.g., `EXECUTE_OPEN_FILE`).
* **`intent`**: Why the user said what they said.
* **`entities`**: Data like file names or subjects. **Note:** Missing values are returned as `null`.

---

## 2. Viora Vision Server (Port 8080)
This server provides the visual intelligence. It describes what the camera sees and automatically translates the description into Egyptian Arabic using the Fanar engine.

### Connection Details
* **Base URL:** `https://8080-01kp795e7c121r8a8jj0d78qwt.cloudspaces.litng.ai`
* **Endpoint:** `/analyze`
* **Protocol:** `HTTP POST (Multipart/Form-Data)`

### Request Structure
This server expects an image file upload:

| Key | Type | Description |
| :--- | :--- | :--- |
| **`file`** | `File (Binary)` | The raw `.jpg` or `.png` frame captured from the camera. |

### Output Fields
* **`status`**: Returns `success` if the image was processed correctly.
* **`viora_reply`**: A natural Egyptian Arabic description of the scene.

---
* **Dependencies:** ```bash
pip install fastapi uvicorn torch transformers requests pydantic pillow arabic-reshaper python-bidi
