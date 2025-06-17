module.exports = {
  testEnvironment: 'jsdom', // pour pouvoir tester le DOM avec react-testing-library
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': 'babel-jest',
  },
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'], // si tu as un fichier de setup
  moduleFileExtensions: ['js', 'jsx', 'json', 'node'],
};
