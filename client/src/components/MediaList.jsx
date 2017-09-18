import React from 'react'
import MediaItem from './MediaItem';

const MediaItemList = ({ records }) => (
  <ul>
    {records.map(record => (
      <MediaItem key={record.id} {...record}  />
    ))}
  </ul>
);

export default MediaItemList;
