import React from 'react';

import {
  Classes
} from '@blueprintjs/core';

import loadWheels from './python/load-wheels.py';


interface IAppRootProps { }
interface IAppRootState extends Readonly<{}> { }

declare let languagePluginLoader: any;
declare let pyodide: any;

class AppRoot extends React.Component<IAppRootProps, IAppRootState> {
  render() {
    return (
      <div className="AppRoot">

      </div>
    );
  }
}

languagePluginLoader.then(() => {
  return Promise.all([
    pyodide.loadPackage(['matplotlib', 'numpy', 'pandas']),
    pyodide.runPython(loadWheels)
  ])
})

let socket = new WebSocket("ws://localhost:8000/api");

export default AppRoot;
