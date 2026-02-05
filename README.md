# synology-tor-client-minimal

Minimal **Tor client (SOCKS proxy)** Docker image designed for **Synology NAS**.  
This container runs a Tor client exposing a SOCKS proxy on port **9150**
(`SocksPort 0.0.0.0:9150`).

---

## 📦 Description

This Docker image:

- is based on **Alpine Linux**
- runs a **headless Tor client** (no GUI)
- exposes a SOCKS proxy for browsers and applications
- is optimized for Docker usage on Synology NAS

---

## 🧩 Versions

- **OS:** Alpine Linux (latest edge)  
  https://alpinelinux.org  
  > Alpine Linux is a security-oriented, lightweight Linux distribution based on musl libc and busybox.

- **tor:** `0.4.8.22-r0`

  https://gitlab.com/torproject/tor

- **lyrebird:** `0.8.1-r2`

  https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/lyrebird

---

## 🚀 Installation & Launch (Synology NAS)

### 1. Start Docker
Open the Synology NAS admin interface and launch the **Docker** package.

### 2. Download the image
Go to the **Registry** tab and search for:

`tor_client_minimal`

Double-click the image to download it.

### 3. Create the container
After the download is complete:

1. Go to the **Image** tab
2. Select the `tor_client_minimal` image
3. Click **Launch** to create the container

### 4. Container configuration
- Set a container name
- Add port mapping:
  - **Local port:** `9150`
  - **Container port:** `9150`

Click **Next**.

### 5. Resource limits (optional)
Adjust CPU and memory limits if needed.  
Click **Next**, then **Apply**.

### 6. Start the container
Launch the container.

---

## 🌐 Usage

Once the container is running:

1. Configure your browser or application to use a **SOCKS proxy**
2. Set:
   - **IP address:** your NAS IP
   - **Port:** `9150`
3. It is recommended to use **Tor Browser** and adjust the connection settings in its preferences

✅ Your Tor client is now running.

---

## 🛡 Notes

- This image runs **Tor client only** (no Tor Browser included)
- It is intended to proxy traffic from other applications through the Tor network

---

## ⚙️ Custom `torrc` configuration (optional)

By default, the container uses the `torrc` file bundled inside the image:

`/etc/tor/torrc`

You can override this configuration by mounting your **own `torrc` file** from the host system (Synology NAS) into the container.

### Why use a custom `torrc`?

This allows you to:

- change Tor network behavior
- enable or disable bridges
- configure pluggable transports (e.g. Lyrebird)
- adjust logging, circuits, exit policies, etc.

### How it works

Docker allows you to bind-mount a file from the host and replace the one inside the container.

Mount your custom `torrc` to: `/etc/tor/torrc`


### Example (Synology Docker UI)

When creating or editing the container:

1. Go to **Volume** settings
2. Add a new mount:
   - **File/Folder (host):** path to your custom `torrc` file  
     (e.g. `/volume1/docker/tor/torrc`)
   - **Mount path (container):** `/etc/tor/torrc`
3. Make sure the file is readable by the `tor` user

Restart the container after applying changes.

### Example (`docker run`)

```bash
docker run -d \
  -p 9150:9150 \
  -v /path/on/host/torrc:/etc/tor/torrc:ro \
  --name tor_client_minimal \
  tor_client_minimal
```

---

## ⚠️ torrc troubleshooting

If your torrc contains errors, Tor will fail to start and the container will exit.
Check container logs for troubleshooting.

---

