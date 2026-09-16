package com.ldleo.mosk

import android.app.AlertDialog
import android.app.Dialog
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.ColorDrawable
import android.os.Bundle
import android.util.Base64
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.view.Window
import android.webkit.*
import android.widget.*
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import androidx.webkit.ProfileStore
import androidx.webkit.ProxyConfig
import androidx.webkit.ProxyController
import androidx.webkit.WebViewCompat
import androidx.webkit.WebViewFeature
import org.json.JSONArray
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.Authenticator
import java.net.HttpURLConnection
import java.net.InetSocketAddress
import java.net.PasswordAuthentication
import java.net.Proxy
import java.net.URL

class MainActivity : AppCompatActivity() {

    private val profiles = mutableListOf<BrowserProfile>()
    private var activeProfile: BrowserProfile? = null
    private var currentCheckId = 0

    // Key Pools & Rotation pointers
    private var proxycheckIndex = 0
    private var scamalyticsIndex = 0

    private lateinit var tvScoreBadge: TextView
    private lateinit var tvVpnStatus: TextView
    private lateinit var btnRefreshIp: TextView
    private lateinit var btnSettingsTop: Button
    private lateinit var btnProfilesSheet: Button
    private lateinit var btnFlashTop: Button
    private lateinit var btnCreateProfileTop: Button
    private lateinit var profilesScreen: LinearLayout
    private lateinit var tvEmptyMessage: TextView
    private lateinit var scrollProfiles: ScrollView
    private lateinit var llProfilesContainer: LinearLayout
    private lateinit var btnFlashSessionBig: Button
    private lateinit var btnNewProfileBig: Button

    private lateinit var browserScreen: LinearLayout
    private lateinit var tvActiveBadge: TextView
    private lateinit var btnMinimize: Button
    private lateinit var btnClean: Button
    private lateinit var webViewContainer: FrameLayout
    private var activeWebView: WebView? = null
    private var currentSheetDialog: Dialog? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        initViews()
        loadProfilesFromPrefs()
        renderProfilesList()

        btnRefreshIp.setOnClickListener { checkIpAndFraudScore() }
        btnSettingsTop.setOnClickListener { showSettingsDialog() }
        btnProfilesSheet.setOnClickListener { showProfilesSheet() }
        btnFlashTop.setOnClickListener { launchFlashSession() }
        btnFlashSessionBig.setOnClickListener { launchFlashSession() }
        btnCreateProfileTop.setOnClickListener { showNewProfileDialog(null) }
        btnNewProfileBig.setOnClickListener { showNewProfileDialog(null) }

        btnMinimize.setOnClickListener { minimizeBrowser() }
        btnClean.setOnClickListener { executeCleanReset() }

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (browserScreen.visibility == View.VISIBLE) {
                    if (activeWebView?.canGoBack() == true) {
                        activeWebView?.goBack()
                    } else {
                        minimizeBrowser()
                    }
                } else {
                    finish()
                }
            }
        })

        checkIpAndFraudScore()
    }

    private fun initViews() {
        tvScoreBadge = findViewById(R.id.tvScoreBadge)
        tvVpnStatus = findViewById(R.id.tvVpnStatus)
        btnRefreshIp = findViewById(R.id.btnRefreshIp)
        btnSettingsTop = findViewById(R.id.btnSettingsTop)
        btnProfilesSheet = findViewById(R.id.btnProfilesSheet)
        btnFlashTop = findViewById(R.id.btnFlashTop)
        btnCreateProfileTop = findViewById(R.id.btnCreateProfileTop)
        profilesScreen = findViewById(R.id.profilesScreen)
        tvEmptyMessage = findViewById(R.id.tvEmptyMessage)
        scrollProfiles = findViewById(R.id.scrollProfiles)
        llProfilesContainer = findViewById(R.id.llProfilesContainer)
        btnFlashSessionBig = findViewById(R.id.btnFlashSessionBig)
        btnNewProfileBig = findViewById(R.id.btnNewProfileBig)

        browserScreen = findViewById(R.id.browserScreen)
        tvActiveBadge = findViewById(R.id.tvActiveBadge)
        btnMinimize = findViewById(R.id.btnMinimize)
        btnClean = findViewById(R.id.btnClean)
        webViewContainer = findViewById(R.id.webViewContainer)
    }

    // --- FRAUD SCORE WITH 6-KEY POOL ROTATION (NO CACHE, 100% REAL-TIME) ---
    private fun loadKeysFromAssets(): Pair<List<String>, List<String>> {
        val p = mutableListOf<String>()
        val s = mutableListOf<String>()
        var sec = ""
        try {
            assets.open("apikeys.txt").bufferedReader().useLines { lines ->
                for (l in lines) {
                    val trim = l.trim()
                    if (trim.isEmpty() || trim.startsWith("#")) continue
                    if (trim == "[proxycheck]") { sec = "p"; continue }
                    if (trim == "[scamalytics]") { sec = "s"; continue }
                    if (sec == "p") p.add(trim)
                    if (sec == "s") s.add(trim)
                }
            }
        } catch (e: Exception) {}
        return Pair(p, s)
    }

    private fun checkIpAndFraudScore() {
        currentCheckId++
        val checkId = currentCheckId

        tvScoreBadge.text = "●"
        tvScoreBadge.setTextColor(Color.parseColor("#FFD60A"))
        tvVpnStatus.text = "🌐 Consultando IP y reputación en vivo..."

        Thread {
            try {
                // 1. Obtener IP publica base y detalles del ISP
                val url = URL("http://ip-api.com/json?fields=status,country,countryCode,query,hosting,proxy,mobile")
                val conn = url.openConnection() as HttpURLConnection
                conn.connectTimeout = 5000
                conn.readTimeout = 5000
                val text = conn.inputStream.bufferedReader().readText()
                conn.disconnect()

                if (checkId != currentCheckId) return@Thread

                val json = JSONObject(text)
                val ip = json.optString("query", "Desconocida")
                val country = json.optString("country", "Desconocido")
                val code = json.optString("countryCode", "")
                val isHosting = json.optBoolean("hosting", false)
                val isProxy = json.optBoolean("proxy", false)
                val isMobile = json.optBoolean("mobile", false)

                val prefs = getSharedPreferences("mosk_settings", Context.MODE_PRIVATE)
                val pKeys = prefs.getString("proxycheck_keys", "")
                    ?.split(",", "\n")?.map { it.trim() }?.filter { it.isNotEmpty() } ?: emptyList()
                val sKeys = prefs.getString("scamalytics_keys", "")
                    ?.split(",", "\n")?.map { it.trim() }?.filter { it.isNotEmpty() } ?: emptyList()

                var finalScore: Int? = null
                var finalSource = ""
                var scoreColor = "#34C759"

                // A. Intentar con Scamalytics (3 cuentas con failover)
                if (sKeys.isNotEmpty()) {
                    for (i in sKeys.indices) {
                        val keyIdx = (scamalyticsIndex + i) % sKeys.size
                        val entry = sKeys[keyIdx]
                        val parts = entry.split(":")
                        if (parts.size == 2) {
                            val user = parts[0].trim()
                            val key = parts[1].trim()
                            try {
                                val sUrl = URL("https://api11.scamalytics.com/\$user/?key=\$key&ip=\$ip")
                                val sConn = sUrl.openConnection() as HttpURLConnection
                                sConn.connectTimeout = 4000
                                sConn.readTimeout = 4000
                                if (sConn.responseCode == 200) {
                                    val sResp = JSONObject(sConn.inputStream.bufferedReader().readText())
                                    if (sResp.optString("status") == "ok") {
                                        finalScore = sResp.optInt("score", 0)
                                        finalSource = "Scamalytics"
                                        scamalyticsIndex = keyIdx
                                        break
                                    }
                                }
                            } catch (e: Exception) {
                                // Fallback a la siguiente key
                            }
                        }
                    }
                }

                // B. Si Scamalytics no está configurado o falló, intentar con Proxycheck (3 cuentas)
                if (finalScore == null && pKeys.isNotEmpty()) {
                    for (i in pKeys.indices) {
                        val keyIdx = (proxycheckIndex + i) % pKeys.size
                        val key = pKeys[keyIdx]
                        try {
                            val pUrl = URL("https://proxycheck.io/v2/\$ip?key=\$key&risk=1&vpn=1")
                            val pConn = pUrl.openConnection() as HttpURLConnection
                            pConn.connectTimeout = 4000
                            pConn.readTimeout = 4000
                            if (pConn.responseCode == 200) {
                                val pResp = JSONObject(pConn.inputStream.bufferedReader().readText())
                                if (pResp.optString("status") == "ok") {
                                    val ipObj = pResp.optJSONObject(ip)
                                    if (ipObj != null) {
                                        finalScore = ipObj.optInt("risk", 0)
                                        finalSource = "Proxycheck"
                                        proxycheckIndex = keyIdx
                                        break
                                    }
                                }
                            }
                        } catch (e: Exception) {
                            // Fallback a la siguiente key
                        }
                    }
                }

                // C. Determinar texto y color definitivo
                val displayText: String
                if (finalScore != null) {
                    displayText = "IP: \$ip | \$country (\$code) | \$finalSource: \$finalScore%"
                    scoreColor = when {
                        finalScore >= 70 -> "#FF453A"
                        finalScore >= 30 -> "#FFD60A"
                        else -> "#34C759"
                    }
                } else {
                    // Fallback directo con datos tecnicos reales
                    val netType = when {
                        isHosting || isProxy -> "Datacenter / VPN"
                        isMobile -> "Red Móvil"
                        else -> "Residencial Limpia"
                    }
                    displayText = "IP: \$ip | \$country (\$code) | \$netType"
                    scoreColor = if (isHosting || isProxy) "#FF453A" else "#34C759"
                }

                runOnUiThread {
                    if (checkId == currentCheckId) {
                        tvVpnStatus.text = displayText
                        tvScoreBadge.text = "●"
                        tvScoreBadge.setTextColor(Color.parseColor(scoreColor))
                    }
                }
            } catch (e: Exception) {
                if (checkId == currentCheckId) {
                    runOnUiThread {
                        tvVpnStatus.text = "⚠️ Red desconectada o tiempo agotado"
                        tvScoreBadge.text = "🔴"
                    }
                }
            }
        }.start()
    }

    private fun showSettingsDialog() {
        val dialog = Dialog(this)
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE)
        dialog.setContentView(R.layout.dialog_settings)
        dialog.window?.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))
        dialog.window?.setLayout((resources.displayMetrics.widthPixels * 0.92).toInt(), ViewGroup.LayoutParams.WRAP_CONTENT)

        val prefs = getSharedPreferences("mosk_settings", Context.MODE_PRIVATE)
        val etProxycheck = dialog.findViewById<EditText>(R.id.etProxycheckKeys)
        val etScamalytics = dialog.findViewById<EditText>(R.id.etScamalyticsKeys)
        val btnSave = dialog.findViewById<Button>(R.id.btnSaveSettings)
        val btnCancel = dialog.findViewById<Button>(R.id.btnCancelSettings)

        etProxycheck.setText(prefs.getString("proxycheck_keys", ""))
        etScamalytics.setText(prefs.getString("scamalytics_keys", ""))

        btnSave.setOnClickListener {
            prefs.edit()
                .putString("proxycheck_keys", etProxycheck.text.toString().trim())
                .putString("scamalytics_keys", etScamalytics.text.toString().trim())
                .apply()
            dialog.dismiss()
            Toast.makeText(this, "Claves guardadas. Consultando en vivo...", Toast.LENGTH_SHORT).show()
            checkIpAndFraudScore()
        }

        btnCancel.setOnClickListener { dialog.dismiss() }
        dialog.show()
    }

    private fun launchFlashSession() {
        currentSheetDialog?.dismiss()
        val randomDev = BrowserProfile.DEVICE_CATALOG.random()
        val seed = (1000..99999).random()
        val flashProfile = BrowserProfile(
            id = "flash_${System.currentTimeMillis()}",
            name = "⚡ Sesión Flash",
            startUrl = "https://browserleaks.com/webgl",
            seed = seed,
            deviceName = randomDev.name,
            gpuVendor = randomDev.gpuVendor,
            gpuRenderer = randomDev.gpuRenderer,
            userAgent = randomDev.userAgent,
            proxyType = "DIRECT",
            proxyHost = "",
            proxyPort = 0,
            proxyUser = "",
            proxyPass = ""
        )
        openProfileSession(flashProfile)
    }

    private fun showNewProfileDialog(profileToEdit: BrowserProfile?) {
        val dialog = Dialog(this)
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE)
        dialog.setContentView(R.layout.dialog_new_profile)
        dialog.window?.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))
        dialog.window?.setLayout((resources.displayMetrics.widthPixels * 0.90).toInt(), ViewGroup.LayoutParams.WRAP_CONTENT)

        val tvTitle = dialog.findViewById<TextView>(R.id.tvDialogTitle)
        val etName = dialog.findViewById<EditText>(R.id.etProfileName)
        val etUrl = dialog.findViewById<EditText>(R.id.etProfileUrl)
        val tvError = dialog.findViewById<TextView>(R.id.tvUrlError)
        val spinnerDevices = dialog.findViewById<Spinner>(R.id.spinnerDevices)
        val btnOpenProxy = dialog.findViewById<LinearLayout>(R.id.btnOpenProxyDialog)
        val tvProxyStatus = dialog.findViewById<TextView>(R.id.tvProxyStatusText)
        val btnSave = dialog.findViewById<Button>(R.id.btnSaveOnly)
        val btnSaveAndOpen = dialog.findViewById<Button>(R.id.btnSaveAndOpen)
        val btnCancel = dialog.findViewById<TextView>(R.id.btnCancelDialog)

        val deviceNames = BrowserProfile.DEVICE_CATALOG.map { it.name }
        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, deviceNames)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        spinnerDevices.adapter = adapter

        var curProxyType = profileToEdit?.proxyType ?: "DIRECT"
        var curProxyHost = profileToEdit?.proxyHost ?: ""
        var curProxyPort = profileToEdit?.proxyPort ?: 0
        var curProxyUser = profileToEdit?.proxyUser ?: ""
        var curProxyPass = profileToEdit?.proxyPass ?: ""

        fun updateProxyDisplay() {
            if (curProxyType != "DIRECT" && curProxyHost.isNotEmpty()) {
                val authNote = if (curProxyUser.isNotEmpty()) " (Auth)" else ""
                tvProxyStatus.text = "$curProxyType://$curProxyHost:$curProxyPort$authNote"
                tvProxyStatus.setTextColor(Color.parseColor("#34C759"))
            } else {
                tvProxyStatus.text = "Sin proxy (Directo)"
                tvProxyStatus.setTextColor(Color.parseColor("#8E8E93"))
            }
        }
        updateProxyDisplay()

        btnOpenProxy.setOnClickListener {
            showProxyConfigDialog(curProxyType, curProxyHost, curProxyPort, curProxyUser, curProxyPass) { type, host, port, user, pass ->
                curProxyType = type
                curProxyHost = host
                curProxyPort = port
                curProxyUser = user
                curProxyPass = pass
                updateProxyDisplay()
            }
        }

        if (profileToEdit != null) {
            tvTitle.text = "Editar perfil"
            etName.setText(profileToEdit.name)
            etUrl.setText(profileToEdit.startUrl)
            val currentIdx = deviceNames.indexOf(profileToEdit.deviceName)
            if (currentIdx >= 0) spinnerDevices.setSelection(currentIdx)
            btnSaveAndOpen.visibility = View.GONE
        }

        fun saveAction(openNow: Boolean) {
            val name = etName.text.toString().trim().ifEmpty { "Perfil ${profiles.size + 1}" }
            val rawUrl = etUrl.text.toString().trim()

            if (!rawUrl.startsWith("http://") && !rawUrl.startsWith("https://")) {
                tvError.visibility = View.VISIBLE
                return
            }
            tvError.visibility = View.GONE

            val selectedDevice = BrowserProfile.DEVICE_CATALOG[spinnerDevices.selectedItemPosition]

            if (profileToEdit != null) {
                profileToEdit.name = name
                profileToEdit.startUrl = rawUrl
                profileToEdit.deviceName = selectedDevice.name
                profileToEdit.gpuVendor = selectedDevice.gpuVendor
                profileToEdit.gpuRenderer = selectedDevice.gpuRenderer
                profileToEdit.userAgent = selectedDevice.userAgent
                profileToEdit.proxyType = curProxyType
                profileToEdit.proxyHost = curProxyHost
                profileToEdit.proxyPort = curProxyPort
                profileToEdit.proxyUser = curProxyUser
                profileToEdit.proxyPass = curProxyPass
                saveProfilesToPrefs()
                renderProfilesList()
            } else {
                val newP = BrowserProfile(
                    id = "profile_${System.currentTimeMillis()}",
                    name = name,
                    startUrl = rawUrl,
                    seed = (1000..99999).random(),
                    deviceName = selectedDevice.name,
                    gpuVendor = selectedDevice.gpuVendor,
                    gpuRenderer = selectedDevice.gpuRenderer,
                    userAgent = selectedDevice.userAgent,
                    proxyType = curProxyType,
                    proxyHost = curProxyHost,
                    proxyPort = curProxyPort,
                    proxyUser = curProxyUser,
                    proxyPass = curProxyPass
                )
                profiles.add(newP)
                saveProfilesToPrefs()
                renderProfilesList()
                if (openNow) openProfileSession(newP)
            }
            dialog.dismiss()
        }

        btnSave.setOnClickListener { saveAction(false) }
        btnSaveAndOpen.setOnClickListener { saveAction(true) }
        btnCancel.setOnClickListener { dialog.dismiss() }
        dialog.show()
    }

    // --- PROXY DIALOG WITH HTTP, HTTPS, SOCKS5, SOCKS4 + AUTH (USER/PASS) ---
    private fun showProxyConfigDialog(
        currentType: String,
        currentHost: String,
        currentPort: Int,
        currentUser: String,
        currentPass: String,
        onSave: (type: String, host: String, port: Int, user: String, pass: String) -> Unit
    ) {
        val dialog = Dialog(this)
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE)
        dialog.setContentView(R.layout.dialog_proxy_config)
        dialog.window?.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))
        dialog.window?.setLayout((resources.displayMetrics.widthPixels * 0.94).toInt(), ViewGroup.LayoutParams.WRAP_CONTENT)

        val rgType = dialog.findViewById<RadioGroup>(R.id.rgProxyType)
        val rbHttp = dialog.findViewById<RadioButton>(R.id.rbHttp)
        val rbHttps = dialog.findViewById<RadioButton>(R.id.rbHttps)
        val rbSocks5 = dialog.findViewById<RadioButton>(R.id.rbSocks5)
        val rbSocks4 = dialog.findViewById<RadioButton>(R.id.rbSocks4)

        val etHost = dialog.findViewById<EditText>(R.id.etProxyServer)
        val etPort = dialog.findViewById<EditText>(R.id.etProxyPort)
        val etUser = dialog.findViewById<EditText>(R.id.etProxyUser)
        val etPass = dialog.findViewById<EditText>(R.id.etProxyPass)
        val btnTest = dialog.findViewById<Button>(R.id.btnTestProxy)
        val tvResult = dialog.findViewById<TextView>(R.id.tvProxyTestResult)
        val btnClear = dialog.findViewById<Button>(R.id.btnClearProxy)
        val btnSave = dialog.findViewById<Button>(R.id.btnSaveProxy)
        val btnCancel = dialog.findViewById<TextView>(R.id.btnCancelProxyDialog)

        when (currentType) {
            "HTTP" -> rbHttp.isChecked = true
            "SOCKS5" -> rbSocks5.isChecked = true
            "SOCKS4" -> rbSocks4.isChecked = true
            else -> rbHttps.isChecked = true
        }

        etHost.setText(currentHost)
        if (currentPort > 0) etPort.setText(currentPort.toString())
        etUser.setText(currentUser)
        etPass.setText(currentPass)

        fun getSelectedType(): String {
            return when (rgType.checkedRadioButtonId) {
                R.id.rbHttp -> "HTTP"
                R.id.rbSocks5 -> "SOCKS5"
                R.id.rbSocks4 -> "SOCKS4"
                else -> "HTTPS"
            }
        }

        btnTest.setOnClickListener {
            val host = etHost.text.toString().trim()
            val portStr = etPort.text.toString().trim()
            val user = etUser.text.toString().trim()
            val pass = etPass.text.toString()

            if (host.isEmpty() || portStr.isEmpty()) {
                tvResult.text = "⚠️ Ingresa servidor y puerto primero"
                tvResult.setTextColor(Color.parseColor("#FFD60A"))
                return@setOnClickListener
            }

            val port = portStr.toIntOrNull() ?: 8080
            val type = getSelectedType()

            tvResult.text = "⏳ Probando conexión y autenticación..."
            tvResult.setTextColor(Color.parseColor("#8E8E93"))

            Thread {
                try {
                    val proxy = if (type.startsWith("SOCKS")) {
                        Proxy(Proxy.Type.SOCKS, InetSocketAddress(host, port))
                    } else {
                        Proxy(Proxy.Type.HTTP, InetSocketAddress(host, port))
                    }

                    if (user.isNotEmpty()) {
                        Authenticator.setDefault(object : Authenticator() {
                            override fun getPasswordAuthentication(): PasswordAuthentication {
                                return PasswordAuthentication(user, pass.toCharArray())
                            }
                        })
                    }

                    val testUrl = URL("http://ip-api.com/json?fields=query,country,countryCode")
                    val conn = testUrl.openConnection(proxy) as HttpURLConnection
                    conn.connectTimeout = 7000
                    conn.readTimeout = 7000

                    if (user.isNotEmpty() && !type.startsWith("SOCKS")) {
                        val authHeader = "Basic " + Base64.encodeToString("$user:$pass".toByteArray(), Base64.NO_WRAP)
                        conn.setRequestProperty("Proxy-Authorization", authHeader)
                    }

                    val response = conn.inputStream.bufferedReader().readText()
                    conn.disconnect()

                    val resJson = JSONObject(response)
                    val outIp = resJson.optString("query")
                    val outCountry = resJson.optString("country")

                    runOnUiThread {
                        tvResult.text = "✅ IP Proxy: $outIp ($outCountry) - ¡Activo!"
                        tvResult.setTextColor(Color.parseColor("#34C759"))
                    }
                } catch (e: Exception) {
                    runOnUiThread {
                        tvResult.text = "❌ Error: ${e.message ?: "Conexión rechazada o credenciales inválidas"}"
                        tvResult.setTextColor(Color.parseColor("#FF453A"))
                    }
                }
            }.start()
        }

        btnSave.setOnClickListener {
            val host = etHost.text.toString().trim()
            val portStr = etPort.text.toString().trim()
            val user = etUser.text.toString().trim()
            val pass = etPass.text.toString()

            if (host.isEmpty() || portStr.isEmpty()) {
                onSave("DIRECT", "", 0, "", "")
            } else {
                onSave(getSelectedType(), host, portStr.toIntOrNull() ?: 8080, user, pass)
            }
            dialog.dismiss()
        }

        btnClear.setOnClickListener {
            onSave("DIRECT", "", 0, "", "")
            dialog.dismiss()
        }

        btnCancel.setOnClickListener { dialog.dismiss() }
        dialog.show()
    }

    private fun openProfileSession(profile: BrowserProfile) {
        activeProfile = profile
        profilesScreen.visibility = View.GONE
        browserScreen.visibility = View.VISIBLE

        tvActiveBadge.text = "🟢 ${profile.name} (${profile.deviceName})"
        webViewContainer.removeAllViews()

        val webView = WebView(this)
        activeWebView = webView
        webViewContainer.addView(
            webView,
            FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
        )

        val settings = webView.settings
        settings.javaScriptEnabled = true
        settings.domStorageEnabled = true
        settings.databaseEnabled = true
        settings.cacheMode = WebSettings.LOAD_DEFAULT
        settings.mediaPlaybackRequiresUserGesture = true
        settings.userAgentString = profile.userAgent

        // Multi-Profile Isolation
        if (WebViewFeature.isFeatureSupported(WebViewFeature.MULTI_PROFILE)) {
            val profileStore = ProfileStore.getInstance()
            val webkitProfile = profileStore.getOrCreateProfile(profile.id)
            webkitProfile.cookieManager.setAcceptCookie(true)
            WebViewCompat.setProfile(webView, webkitProfile.name)
        }

        // Configurar Proxy
        if (profile.proxyType != "DIRECT" && profile.proxyHost.isNotEmpty() && profile.proxyPort > 0) {
            if (WebViewFeature.isFeatureSupported(WebViewFeature.PROXY_OVERRIDE)) {
                val scheme = when (profile.proxyType) {
                    "SOCKS5", "SOCKS4" -> "socks"
                    "HTTPS" -> "https"
                    else -> "http"
                }
                val proxyUrl = "$scheme://${profile.proxyHost}:${profile.proxyPort}"
                val config = ProxyConfig.Builder()
                    .addProxyRule(proxyUrl)
                    .build()
                ProxyController.getInstance().setProxyOverride(config, { it.run() }, {})
            }
        } else {
            if (WebViewFeature.isFeatureSupported(WebViewFeature.PROXY_OVERRIDE)) {
                ProxyController.getInstance().clearProxyOverride({ it.run() }, {})
            }
        }

        webView.webViewClient = object : WebViewClient() {
            override fun onPageStarted(view: WebView?, url: String?, favicon: Bitmap?) {
                super.onPageStarted(view, url, favicon)
                val script = StealthScript.generate(profile.seed, profile.gpuVendor, profile.gpuRenderer, profile.userAgent)
                view?.evaluateJavascript(script, null)
            }

            override fun onReceivedHttpAuthRequest(view: WebView?, handler: HttpAuthHandler?, host: String?, realm: String?) {
                if (profile.proxyUser.isNotEmpty()) {
                    handler?.proceed(profile.proxyUser, profile.proxyPass)
                } else {
                    super.onReceivedHttpAuthRequest(view, handler, host, realm)
                }
            }

            override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                val targetUrl = request?.url?.toString() ?: return false
                view?.loadUrl(targetUrl)
                return true
            }
        }

        webView.webChromeClient = object : WebChromeClient() {
            override fun onPermissionRequest(request: PermissionRequest?) {
                request?.deny()
            }
        }

        webView.loadUrl(profile.startUrl)
    }

    private fun minimizeBrowser() {
        browserScreen.visibility = View.GONE
        profilesScreen.visibility = View.VISIBLE
    }

    private fun executeCleanReset() {
        activeProfile?.let { profile ->
            if (WebViewFeature.isFeatureSupported(WebViewFeature.MULTI_PROFILE)) {
                val profileStore = ProfileStore.getInstance()
                val webkitProfile = profileStore.getProfile(profile.id)
                webkitProfile?.cookieManager?.removeAllCookies(null)
                webkitProfile?.webStorage?.deleteAllData()
            }
            activeWebView?.clearCache(true)
            activeWebView?.clearHistory()

            // 1. Regenerar semilla unica para Canvas y Audio
            profile.seed = (1000..99999).random()

            // 2. Rotar dispositivo
            val randomDev = BrowserProfile.DEVICE_CATALOG.random()
            profile.deviceName = randomDev.name
            profile.gpuVendor = randomDev.gpuVendor
            profile.gpuRenderer = randomDev.gpuRenderer
            profile.userAgent = randomDev.userAgent
            activeWebView?.settings?.userAgentString = profile.userAgent

            saveProfilesToPrefs()
            renderProfilesList()

            tvActiveBadge.text = "🟢 ${profile.name} (Rotado: ${profile.deviceName})"
            activeWebView?.reload()
            Toast.makeText(this, "Clean completado: Canvas, Audio y Perfil renovados", Toast.LENGTH_SHORT).show()
        }
    }

    private fun showProfilesSheet() {
        val dialog = Dialog(this)
        currentSheetDialog = dialog
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE)
        dialog.setContentView(R.layout.sheet_profiles)
        dialog.window?.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))
        dialog.window?.setLayout(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
        dialog.window?.setGravity(Gravity.BOTTOM)

        val llContainer = dialog.findViewById<LinearLayout>(R.id.llSheetProfiles)
        val btnNew = dialog.findViewById<Button>(R.id.btnSheetNewProfile)

        btnNew.setOnClickListener {
            dialog.dismiss()
            showNewProfileDialog(null)
        }

        llContainer.removeAllViews()
        for (p in profiles) {
            val card = LinearLayout(this)
            card.orientation = LinearLayout.HORIZONTAL
            card.setBackgroundResource(R.drawable.bg_card)
            card.setPadding(16, 16, 16, 16)
            val lp = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
            lp.setMargins(0, 0, 0, 10)
            card.layoutParams = lp
            card.gravity = Gravity.CENTER_VERTICAL

            val info = LinearLayout(this)
            info.orientation = LinearLayout.VERTICAL
            val infoLp = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
            info.layoutParams = infoLp

            val title = TextView(this)
            title.text = p.name
            title.setTextColor(Color.parseColor("#F0F0F0"))
            title.textSize = 15f
            title.typeface = Typeface.DEFAULT_BOLD

            val sub = TextView(this)
            val authNote = if (p.proxyUser.isNotEmpty()) " (Auth)" else ""
            val proxyStr = if (p.proxyType != "DIRECT" && p.proxyHost.isNotEmpty()) "${p.proxyType}://${p.proxyHost}:${p.proxyPort}$authNote" else "Directo"
            sub.text = "${p.deviceName} • $proxyStr"
            sub.setTextColor(Color.parseColor("#8E8E93"))
            sub.textSize = 12f

            info.addView(title)
            info.addView(sub)

            val btnOpen = Button(this)
            btnOpen.text = "Abrir"
            btnOpen.textSize = 12f
            btnOpen.setTextColor(Color.parseColor("#000000"))
            btnOpen.setBackgroundColor(Color.parseColor("#C5B3F9"))
            btnOpen.setOnClickListener {
                dialog.dismiss()
                openProfileSession(p)
            }

            val btnEdit = TextView(this)
            btnEdit.text = "✏️"
            btnEdit.setPadding(12, 8, 12, 8)
            btnEdit.textSize = 14f
            btnEdit.setOnClickListener {
                dialog.dismiss()
                showNewProfileDialog(p)
            }

            val btnDel = TextView(this)
            btnDel.text = "🗑️"
            btnDel.setPadding(8, 8, 8, 8)
            btnDel.textSize = 14f
            btnDel.setOnClickListener {
                AlertDialog.Builder(this)
                    .setTitle("Eliminar perfil")
                    .setMessage("¿Deseas eliminar '${p.name}'?")
                    .setPositiveButton("Eliminar") { _, _ ->
                        profiles.remove(p)
                        saveProfilesToPrefs()
                        renderProfilesList()
                        dialog.dismiss()
                    }
                    .setNegativeButton("Cancelar", null)
                    .show()
            }

            card.addView(info)
            card.addView(btnOpen)
            card.addView(btnEdit)
            card.addView(btnDel)
            llContainer.addView(card)
        }
        dialog.show()
    }

    private fun renderProfilesList() {
        llProfilesContainer.removeAllViews()
        if (profiles.isEmpty()) {
            tvEmptyMessage.visibility = View.VISIBLE
            scrollProfiles.visibility = View.GONE
        } else {
            tvEmptyMessage.visibility = View.GONE
            scrollProfiles.visibility = View.VISIBLE

            for (p in profiles) {
                val card = LinearLayout(this)
                card.orientation = LinearLayout.HORIZONTAL
                card.setBackgroundResource(R.drawable.bg_card)
                card.setPadding(20, 20, 20, 20)
                val lp = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
                lp.setMargins(0, 0, 0, 14)
                card.layoutParams = lp
                card.gravity = Gravity.CENTER_VERTICAL
                card.isClickable = true
                card.isFocusable = true

                val info = LinearLayout(this)
                info.orientation = LinearLayout.VERTICAL
                val infoLp = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
                info.layoutParams = infoLp

                val title = TextView(this)
                title.text = p.name
                title.setTextColor(Color.parseColor("#F0F0F0"))
                title.textSize = 16f
                title.typeface = Typeface.DEFAULT_BOLD

                val sub = TextView(this)
                val authNote = if (p.proxyUser.isNotEmpty()) " (Auth)" else ""
                val proxyStr = if (p.proxyType != "DIRECT" && p.proxyHost.isNotEmpty()) "${p.proxyType}://${p.proxyHost}:${p.proxyPort}$authNote" else "Directo"
                sub.text = "${p.deviceName}
$proxyStr"
                sub.setTextColor(Color.parseColor("#8E8E93"))
                sub.textSize = 12f

                info.addView(title)
                info.addView(sub)

                val btnOpen = Button(this)
                btnOpen.text = "Abrir"
                btnOpen.textSize = 12f
                btnOpen.setTextColor(Color.parseColor("#000000"))
                btnOpen.setBackgroundColor(Color.parseColor("#C5B3F9"))
                btnOpen.setOnClickListener { openProfileSession(p) }

                val btnEdit = TextView(this)
                btnEdit.text = "✏️"
                btnEdit.setPadding(12, 8, 12, 8)
                btnEdit.textSize = 14f
                btnEdit.setOnClickListener { showNewProfileDialog(p) }

                val btnDel = TextView(this)
                btnDel.text = "🗑️"
                btnDel.setPadding(8, 8, 8, 8)
                btnDel.textSize = 14f
                btnDel.setOnClickListener {
                    AlertDialog.Builder(this)
                        .setTitle("Eliminar perfil")
                        .setMessage("¿Deseas eliminar '${p.name}'?")
                        .setPositiveButton("Eliminar") { _, _ ->
                            profiles.remove(p)
                            saveProfilesToPrefs()
                            renderProfilesList()
                        }
                        .setNegativeButton("Cancelar", null)
                        .show()
                }

                card.addView(info)
                card.addView(btnOpen)
                card.addView(btnEdit)
                card.addView(btnDel)
                llProfilesContainer.addView(card)
            }
        }
    }

    private fun saveProfilesToPrefs() {
        val prefs = getSharedPreferences("browser_profiles", MODE_PRIVATE)
        val array = JSONArray()
        for (p in profiles) {
            array.put(p.toJson())
        }
        prefs.edit().putString("profiles_list", array.toString()).apply()
    }

    private fun loadProfilesFromPrefs() {
        profiles.clear()
        val prefs = getSharedPreferences("browser_profiles", MODE_PRIVATE)
        val raw = prefs.getString("profiles_list", null) ?: return
        try {
            val array = JSONArray(raw)
            for (i in 0 until array.length()) {
                profiles.add(BrowserProfile.fromJson(array.getJSONObject(i)))
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    override fun onPause() {
        super.onPause()
        activeWebView?.let {
            it.onPause()
            it.pauseTimers()
        }
        if (WebViewFeature.isFeatureSupported(WebViewFeature.MULTI_PROFILE)) {
            activeProfile?.let { profile ->
                ProfileStore.getInstance().getProfile(profile.id)?.cookieManager?.flush()
            }
        }
    }
}