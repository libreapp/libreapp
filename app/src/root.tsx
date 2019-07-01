import React from 'react';

import {
  Classes
} from '@blueprintjs/core';

import loadWheels from './python/load-wheels.py';


interface IAppRootProps { }
interface IAppRootState extends Readonly<{}> { }

declare let languagePluginLoader: any;
declare let pyodide: any;
declare let Module: any;

class AppRoot extends React.Component<IAppRootProps, IAppRootState> {
  render() {
    return (
      <div className="AppRoot">

      </div>
    );
  }
}

const pythonReady = languagePluginLoader.then(() => {
  return Promise.all([
    pyodide.loadPackage(['matplotlib', 'numpy', 'pandas']),
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

    const root = document.getElementsByClassName("AppRoot")[0];
    root.innerHTML = header;
  })
}

export default AppRoot;
