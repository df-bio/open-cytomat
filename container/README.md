# open-cytomat SiLA2 Docker server

Docker-only runtime for the open-cytomat SiLA2 plate-movement server.

## Start server

Set the serial port/device and start:

```bash
export CYTOMAT_SERIAL_PORT=/dev/ttyUSB0
export CYTOMAT_DEVICE=/dev/ttyUSB0
just -f container/Justfile up
```

Server endpoint:

- `localhost:50052`

Logs:

```bash
just -f container/Justfile logs
```

Stop:

```bash
just -f container/Justfile down
```

## Notes

- SiLA2 is installed via package extra (`.[sila]`) in this image.
- Base package installs can omit SiLA2 dependency.
- TLS mode uses packaged cert/key from `src/cytomat/sila2_adapter/certs/` when `--insecure` is not set.
