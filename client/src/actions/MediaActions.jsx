import { CREATE_MEDIA, READ_MEDIA, UPDATE_MEDIA, DELETE_MEDIA } from '../constants/MediaTypes';
1
export function createMedia(data) {
  return {
    type: CREATE_MEDIA,
    data,
  };
}

export function readMedia() {
  return {
    type: READ_MEDIA,
  };
}

export function updateMedia(id, data) {
  return {
    type: UPDATE_MEDIA,
    id,
    data
  };
}

export function deleteMedia(id) {
  return {
    type: DELETE_MEDIA,
    id
  };
}
