# Sprint 2

Daniel White, daniel-white99, PyTris
(include your name, github id, and group name here)

### What you planned to do

- Format JSON object to send/recive player info and locked positions on game board. Issue #25: https://github.com/utk-cs340-fall22/PyTris/issues/25
- Encode JSON object to send player info to server, specifically locked positions into a 1D Array of pixels. Issue #26: https://github.com/utk-cs340-fall22/PyTris/issues/26
- Decode JSON object to recive opponent info from server, specifically oreienting the 1D Array of pixels into a local grid map. Issue #27: https://github.com/utk-cs340-fall22/PyTris/issues/27






### What you did not do
I accomplished all my planned issues.

### What problems you encountered

- JSON objects cannot be made from dictionaries of tuples, this made the JSON formatting much more difficult.
- Encoding and Decoding the locked positions needed a new class of playerinfo in order to send the data over a JSON correctly.
- The encoding needed to format the JSON string requires a 2D array which can be of O(n^2) time.

### Issues you worked on
- [#25](https://github.com/utk-cs340-fall22/PyTris/issues/25) JSON Formatting.
- [#26](https://github.com/utk-cs340-fall22/PyTris/issues/26) JSON Encoding.
- [#27](https://github.com/utk-cs340-fall22/PyTris/issues/27) JSON Decoding.

### Files you worked on
- PyTris/pytris.py 

### What you accomplished

During sprint2 I was able to complete all my assigned tasks and format JSON objects in order to be sent and recieved over the server socket. To format a JSON object, a encode and decode function was needed in order to properly send and recive data that can be used by the pytris client. 