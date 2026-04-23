#  Viora NLU Server 
This server is the brain that converts user speech/text into system actions. Use this guide to connect your backend service to the NLU engine.

---

## Connection Details
* **Base URL:** `https://8000-01kp795e7c121r8a8jj0d78qwt.cloudspaces.litng.ai`
* **Endpoint:** `/api/v1/parse`
* **Protocol:** HTTP POST (JSON)

---

##  Request Structure
Your app must send a JSON body with the following format:

| Key | Type | Description |
| :--- | :--- | :--- |
| `text` | `string` | The user's voice command or typed message. |


---

## Response Structure 


### 1. The Output Fields
* **`viora_reply`**: The actual string to speak or display.
* **`decision`**: The system code that tells your app what to do next.
* **`intent`**: Why the user said what they said.

### 2. Decision Action Codes
| Action Code | Hardware Instruction |
| :--- | :--- |
| `EXECUTE_CAMERA_START` | Power on the camera feed. |
| `EXECUTE_CAMERA_STOP` | Shut down the camera hardware. |
| `EXECUTE_SCENE_DESCRIPTION` | Snapshot a frame and describe it. |
| `EXECUTE_CAMERA_SCAN` | Extract text from the current view (OCR). |

---