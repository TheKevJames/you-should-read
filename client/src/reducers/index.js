import { combineReducers } from 'redux'
import MediaReducer from 'reducers/MediaReducer';

const reducer = combineReducers({
  media: MediaReducer
});

export default reducer;
