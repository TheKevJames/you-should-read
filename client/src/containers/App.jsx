import React from 'react';
import { connect } from 'react-redux';
import MediaList from 'components/MediaList';

const MediaPage = ({records, actions}) => (
  <div>
    This is a test
    <MediaList records={records} actions={actions} />
  </div>
);

const mapStateToProps = state => {
  return {
    records: state.media
  };
};


const App = connect(
  mapStateToProps,
)(MediaPage);

export default App;
