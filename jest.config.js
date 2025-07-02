module.exports = {
  transform: {
    '^.+\\.(ts|tsx)$': 'babel-jest',
  },
  testEnvironment: 'jsdom',
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx'],
  testMatch: ['**/?(*.)+(spec|test).[jt]s?(x)'],
  moduleNameMapper: {
    '\\.module\\.css$': '<rootDir>/jest-css-modules.mock.js',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy'  // optional, for other CSS files
  },
  roots: ['<rootDir>/frontend'],
};
