import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 20,
    paddingVertical: 20,
    backgroundColor: '#1D1D2B',
    alignItems: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#B43CFF',
    marginTop: 30,
    marginBottom: 20,
    textAlign: 'center',
  },
  bookCover: {
    width: 280,
    height: 400,
    resizeMode: 'cover',
    borderRadius: 12,
    marginBottom: 20,
  },
  descriptionContainer: {
    marginVertical: 20,
  },
  text: {
    fontSize: 18,
    color: '#EEEEEE',
    marginVertical: 8,
    textAlign: 'center',
    lineHeight: 26,
  },
  boldText: {
    fontWeight: 'bold',
    fontSize: 18,
    color: '#EEEEEE',
    marginVertical: 8,
    textAlign: 'center',
    lineHeight: 26,
  },
  cursiveText: {
    fontSize: 18,
    color: '#EEEEEE',
    marginVertical: 8,
    textAlign: 'center',
    lineHeight: 26,
    fontStyle: 'italic',
  },
  ratingContainer: {
    flexDirection: 'row',
    marginTop: 10,
    marginBottom: 20,
  },
  button: {
    backgroundColor: '#B43CFF',
    paddingVertical: 14,
    paddingHorizontal: 28,
    borderRadius: 10,
    marginTop: 20,
    marginBottom: 30, // Agregar margen inferior
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.4,
    shadowRadius: 6,
    elevation: 6,
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: '600',
    textAlign: 'center',
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.6)',
  },
  map: {
    width: '100%',
    height: '70%',
    borderRadius: 16,
    overflow: 'hidden',
  },
  modalActions: {
    backgroundColor: '#1D1D2B',
    paddingVertical: 14,
    paddingHorizontal: 20,
    width: '100%',
    flexDirection: 'row',
    justifyContent: 'space-around',
    borderTopLeftRadius: 16,
    borderTopRightRadius: 16,
  },
});

export default styles;
