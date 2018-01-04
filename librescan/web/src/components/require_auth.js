import React, { Component } from 'react';
import {connect} from 'react-redux';

export default function(ComposedComponent) {
  class Authentication extends Component {
    render() {
      return <ComposedComponent {...this.props} />
    }
  }

  function mapStateToProps({authenticated}) {
    return {authenticated};
  }

  return connect(mapStateToProps)(Authentication);
}
