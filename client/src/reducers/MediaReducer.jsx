import { CREATE_MEDIA, READ_MEDIA, UPDATE_MEDIA, DELETE_MEDIA } from 'constants/MediaTypes';

const dummyData = [
  {
    'id': 42,
    'name': "Hitchhiker's Guide to the Galaxy",
    'url': 'https://hitchhikersguide.com/',
    'rating': 9.3297,
    'created_at': 1502680672,
    'updated_at': 1502680672
  }, {
    'id': 1,
    'name': "Skullduggery Pleasant",
    'url': 'http://www.skulduggerypleasant.co.uk',
    'rating': 5.8297,
    'created_at': 1502680672,
    'updated_at': 1502680672
  },{
    'id': 2,
    'name': "Mistborn",
    'url': 'https://brandonsanderson.com/books/mistborn/the-final-empire/',
    'rating': 3.8297,
    'created_at': 1502680672,
    'updated_at': 1502680672
  }
];



function createMedia(state, data) {
  return [
    ...state,
  ];
}

function updateMedia(state, id, data) {
  return [
    ...state,
  ];
}


function readMedia(state) {
  return [
    ...state,
  ];
}

function deleteMedia(state, id) {
  return [
    ...state,
  ];
}

export default function MediaReducer(state = dummyData, action) {
  switch(action.type) {
    case CREATE_MEDIA:
      return createMedia(state, action.data);
    case READ_MEDIA:
      return readMedia(state);
    case UPDATE_MEDIA:
      return updateMedia(state, action.id, action.data);
    case DELETE_MEDIA:
      return deleteMedia(state, action.id);
    default:
      return state;
  }

}
