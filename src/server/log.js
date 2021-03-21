const { createLogger, format, transports } = require('winston');

const fmt = format.printf(({
  level,
  message,
  label,
  timestamp,
}) => `${timestamp} [${label}] ${level}: ${JSON.stringify(message)}`);

const logger = createLogger({
  format: format.combine(
    format.label({ label: 'javpy' }),
    format.timestamp(),
    fmt,
  ),
  transports: [new transports.Console()],
});

module.exports = {
  logger,
};
