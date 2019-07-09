import React from 'react';

import '../pyodide/init'


interface IAppComponentProps { }
interface IAppComponentState extends Readonly<{}> { }


class AppComponent extends React.Component<IAppComponentProps, IAppComponentState> {
  render() {
    return (
      <div className="AppComponent">

      </div>
    );
  }
}

export default AppComponent;
