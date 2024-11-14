import React from 'react';
import { View, Text } from 'react-native';

interface StarRatingProps {
  rating: number;
  size?: number;
  color?: string;
}

export const StarRating: React.FC<StarRatingProps> = ({ rating, size = 20, color = '#FFDF00' }) => {
  const fullStars = Math.floor(rating);
  const hasHalfStar = rating - fullStars >= 0.5;

  const stars = [];
  for (let i = 0; i < fullStars; i++) {
    stars.push(<Text key={`full-${i}`} style={{ fontSize: size, color }}>★</Text>);
  }
  if (hasHalfStar) {
    stars.push(<Text key="half" style={{ fontSize: size, color }}>☆</Text>);
  }

  return <View style={{ flexDirection: 'row' }}>{stars}</View>;
};
