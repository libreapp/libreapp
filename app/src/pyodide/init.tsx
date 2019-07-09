import loadWheels from './load-wheels.py';

declare let languagePluginLoader: any;
declare let pyodide: any;
declare let Module: any;

const pythonReady = languagePluginLoader.then(() => {
  return Promise.all([
    pyodide.runPython(loadWheels)
  ])
})

let socket = new WebSocket("ws://127.0.0.1:29285/api");

socket.onmessage = (event) => {
  console.log(event)

  const messageData: Blob = event.data
  const arrayBuffer = new Response(messageData).arrayBuffer();

  Promise.all([arrayBuffer, pythonReady]).then(([array,]) => {
    Module['FS_createDataFile']('/', 'temp.dcm', new Uint8Array(array), true, true, true);

    const header: string = pyodide.runPython(`
import pydicom
repr(pydicom.dcmread('temp.dcm', force=True))`)

    const root = document.getElementsByClassName("AppComponent")[0];
    root.innerHTML = header;
  })
}
