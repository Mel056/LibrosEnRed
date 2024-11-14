import React, {useState, useEffect} from 'react';
import {View, Text, TouchableOpacity, Modal, Button, Image} from 'react-native';
import MapView, {Marker, Circle, LatLng} from 'react-native-maps';
import Geolocation from 'react-native-geolocation-service';
import {StarRating} from './components/ui/StarRating';
import styles from './styles/bookDetailStyles';
import {PermissionsAndroid} from 'react-native';

interface Location {
  latitude: number;
  longitude: number;
}

const BookDetailScreen: React.FC = () => {
  const [isModalVisible, setIsModalVisible] = useState<boolean>(false);
  const [selectedLocation, setSelectedLocation] = useState<Location | null>(
    null,
  );
  const [confirmLocation, setConfirmLocation] = useState<boolean>(false);
  const [userLocation, setUserLocation] = useState<Location | null>(null);

  useEffect(() => {
    requestLocationPermission();
  }, []);

  const requestLocationPermission = async () => {
    try {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
        {
          title: 'Location Permission',
          message:
            'We need access to your location to show your current position.',
          buttonNeutral: 'Ask Me Later',
          buttonNegative: 'Cancel',
          buttonPositive: 'OK',
        },
      );
      if (granted === PermissionsAndroid.RESULTS.GRANTED) {
        console.log('You can use the location');
        getUserLocation();
      } else {
        console.log('Location permission denied');
      }
    } catch (err) {
      console.warn(err);
    }
  };

  const getUserLocation = () => {
    Geolocation.getCurrentPosition(
      position => {
        const {latitude, longitude} = position.coords;
        setUserLocation({latitude, longitude});
      },
      error => {
        console.log(error);
      },
      {enableHighAccuracy: true, timeout: 15000, maximumAge: 10000},
    );
  };

  const handleRequestExchange = () => {
    setIsModalVisible(true);
  };

  const handleMapPress = (e: any) => {
    const coordinate: LatLng = e.nativeEvent.coordinate;
    setSelectedLocation(coordinate);
  };

  const handleConfirmLocation = () => {
    setConfirmLocation(true);
    setIsModalVisible(false);
    console.log('Confirmed location:', selectedLocation);
  };

  return (
    <View style={styles.container}>
      {/* Title */}
      <Text style={styles.title}>Don Quijote de la Mancha</Text>

      {/* Book Cover */}
      <Image
        source={{
          uri: 'https://i1.whakoom.com/large/0a/36/df423bd060e44acb88930d9cc139fb28.jpg',
        }}
        style={styles.bookCover}
      />

      {/* Description */}
      <View style={styles.descriptionContainer}>
        <Text>
          <Text style={styles.boldText}>Autor:</Text>
          <Text style={styles.text}> Miguel de Cervantes</Text>
        </Text>{' '}
        <Text style={styles.cursiveText}>
          Un libro clásico sobre las aventuras de Don Quijote.
        </Text>
      </View>

      {/* Rating */}
      <View style={styles.ratingContainer}>
        <StarRating rating={4.5} size={24} color="#B43CFF" />
      </View>

      {/* Exchange Request Button */}
      <TouchableOpacity style={styles.button} onPress={handleRequestExchange}>
        <Text style={styles.buttonText}>Solicitar intercambio</Text>
      </TouchableOpacity>

      {/* Location Selection Modal */}
      {isModalVisible && (
        <Modal
          transparent={true}
          visible={isModalVisible}
          animationType="slide">
          <View style={styles.modalContainer}>
            <MapView
              style={styles.map}
              initialRegion={
                userLocation
                  ? {
                      latitude: userLocation.latitude,
                      longitude: userLocation.longitude,
                      latitudeDelta: 0.0922,
                      longitudeDelta: 0.0421,
                    }
                  : undefined
              }
              onPress={handleMapPress}>
              {userLocation && (
                <Circle
                  center={{
                    latitude: userLocation.latitude,
                    longitude: userLocation.longitude,
                  }}
                  radius={1000}
                  strokeWidth={2}
                  strokeColor="#B43CFF"
                  fillColor="rgba(180,60,255,0.3)"
                />
              )}
              {selectedLocation && <Marker coordinate={selectedLocation} />}
            </MapView>
            <View style={styles.modalActions}>
              <Button
                title="Confirmar"
                onPress={handleConfirmLocation}
                color="#B43CFF"
              />
              <Button
                title="Cancelar"
                onPress={() => setIsModalVisible(false)}
                color="#666"
              />
            </View>
          </View>
        </Modal>
      )}
    </View>
  );
};

export default BookDetailScreen;
