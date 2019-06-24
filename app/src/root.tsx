import React from 'react';

import {
  Classes
} from '@blueprintjs/core';


interface IAppRootProps { }
interface IAppRootState extends Readonly<{}> { }

class AppRoot extends React.Component<IAppRootProps, IAppRootState> {
  render() {
    return (
      <div className="AppRoot">

      </div>
    );
  }
}

export default AppRoot;
