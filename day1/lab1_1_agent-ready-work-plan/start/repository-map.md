# Repository Map

| Path | Purpose | Boundary note |
| :--- | :--- | :--- |
| `schemas/shipment-event.json` | Shared event contract | Structural hub; approve first |
| `channels/email.py` | Email rendering | Email bounded context |
| `channels/sms.py` | Short-message rendering | Messaging bounded context |
| `preferences/reader.py` | Channel preference lookup | Customer bounded context |
| `audit/recorder.py` | Notification audit records | Compliance bounded context |
| `router.py` | Coordinates all notification paths | Structural hub; one integration owner |
| `tests/test_notifications.py` | Full integration acceptance | Integration owner only |

Platform authentication, gateways, service meshes, and vendor delivery clients are outside the lab scope.
