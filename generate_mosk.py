import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("app/src/main/java/com/ldleo/mosk", exist_ok=True)
os.makedirs("app/src/main/res/layout", exist_ok=True)
os.makedirs("app/src/main/res/values", exist_ok=True)
os.makedirs("app/src/main/res/drawable", exist_ok=True)
os.makedirs("app/src/main/assets", exist_ok=True)
# Si existe apikeys.txt en la raiz del repo, usarlo directamente
if os.path.exists("apikeys.txt"):
    import shutil
    shutil.copy("apikeys.txt", "app/src/main/assets/apikeys.txt")
elif not os.path.exists("app/src/main/assets/apikeys.txt"):
    with open("app/src/main/assets/apikeys.txt", "w") as f:
        f.write("""# Mosk API Keys Pool (3 Proxycheck + 3 Scamalytics)
[proxycheck]
# Pega aqui tus 3 claves de proxycheck (1 por linea)

[scamalytics]
# Pega aqui tus 3 cuentas de scamalytics en formato usuario:key (1 por linea)
""")

sizes = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192
}

for folder, size in sizes.items():
    os.makedirs(f"app/src/main/res/{folder}", exist_ok=True)
    font = None
    for fpath in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    ):
        if os.path.exists(fpath):
            font = ImageFont.truetype(fpath, int(size * 0.23))
            break
    if not font:
        font = ImageFont.load_default()

    text = "MOSK"
    box = (2, 2, size - 3, size - 3)

    # Adaptive / Square Icon
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(box, radius=size // 4, fill=(225, 25, 25, 255), outline=(175, 15, 15, 255), width=max(1, size // 48))
    b0, b1, b2, b3 = draw.textbbox((0, 0), text, font=font)
    w, h = b2 - b0, b3 - b1
    x = (size - w) / 2
    y = (size - h) / 2 - b1
    draw.text((x, y), text, fill=(12, 12, 12, 255), font=font)
    img.save(f"app/src/main/res/{folder}/ic_launcher.png")

    # Round Icon
    rimg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    rdraw = ImageDraw.Draw(rimg)
    rdraw.ellipse(box, fill=(225, 25, 25, 255), outline=(175, 15, 15, 255), width=max(1, size // 48))
    rdraw.text((x, y), text, fill=(12, 12, 12, 255), font=font)
    rimg.save(f"app/src/main/res/{folder}/ic_launcher_round.png")

with open("settings.gradle", "w") as f:
    f.write("""pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "Mosk"
include ':app'
""")

with open("build.gradle", "w") as f:
    f.write("""plugins {
    id 'com.android.application' version '8.2.2' apply false
    id 'org.jetbrains.kotlin.android' version '1.9.22' apply false
}
""")

with open("app/build.gradle", "w") as f:
    f.write("""plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.ldleo.mosk'
    compileSdk 34

    defaultConfig {
        applicationId "com.ldleo.mosk"
        minSdk 26
        targetSdk 34
        versionCode 2
        versionName "2.1"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = '17'
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.webkit:webkit:1.12.1'
}
""")

with open("app/src/main/AndroidManifest.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:label="Mosk"
        android:supportsRtl="true"
        android:theme="@style/Theme.Mosk"
        android:usesCleartextTraffic="true">
        <activity
            android:name=".MainActivity"
            android:configChanges="orientation|screenSize|keyboardHidden"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>""")

with open("app/src/main/res/values/strings.xml", "w") as f:
    f.write("""<resources>
    <string name="app_name">Mosk</string>
</resources>""")

with open("app/src/main/res/values/colors.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="bg_black">#0D0D0D</color>
    <color name="card_dark">#181818</color>
    <color name="card_border">#2A2A2A</color>
    <color name="text_primary">#F0F0F0</color>
    <color name="text_secondary">#8E8E93</color>
    <color name="accent_purple">#C5B3F9</color>
    <color name="accent_green">#34C759</color>
    <color name="accent_red">#FF453A</color>
    <color name="accent_yellow">#FFD60A</color>
</resources>""")

with open("app/src/main/res/values/themes.xml", "w") as f:
    f.write("""<resources>
    <style name="Theme.Mosk" parent="Theme.Material3.Dark.NoActionBar">
        <item name="android:statusBarColor">@color/bg_black</item>
        <item name="android:navigationBarColor">@color/bg_black</item>
    </style>
</resources>""")

with open("app/src/main/res/drawable/bg_card.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/card_dark" />
    <corners android:radius="14dp" />
    <stroke android:width="1dp" android:color="@color/card_border" />
</shape>""")

with open("app/src/main/res/drawable/bg_input.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#242424" />
    <corners android:radius="10dp" />
    <stroke android:width="1dp" android:color="#383838" />
</shape>""")

with open("app/src/main/res/drawable/bg_sheet.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#141414" />
    <corners android:topLeftRadius="20dp" android:topRightRadius="20dp" />
    <stroke android:width="1dp" android:color="#2C2C2C" />
</shape>""")

with open("app/src/main/res/layout/activity_main.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:background="@color/bg_black">

    <LinearLayout
        android:id="@+id/ipBanner"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:background="#121212"
        android:padding="8dp"
        android:gravity="center_vertical">

        <TextView
            android:id="@+id/tvScoreBadge"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="●"
            android:textColor="@color/accent_yellow"
            android:textSize="14sp"
            android:paddingEnd="6dp" />

        <TextView
            android:id="@+id/tvVpnStatus"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="🌐 Verificando red y reputación..."
            android:textColor="@color/text_secondary"
            android:textSize="12sp" />

        <TextView
            android:id="@+id/btnRefreshIp"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="🔄"
            android:padding="4dp"
            android:textSize="14sp" />
    </LinearLayout>

    <LinearLayout
        android:id="@+id/topBar"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:padding="10dp"
        android:background="@color/card_dark"
        android:gravity="center_vertical">

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Mosk"
            android:textColor="@color/text_primary"
            android:textSize="18sp"
            android:textStyle="bold" />

        <View
            android:layout_width="0dp"
            android:layout_height="1dp"
            android:layout_weight="1" />

        <Button
            android:id="@+id/btnSettingsTop"
            android:layout_width="38dp"
            android:layout_height="36dp"
            android:text="⚙️"
            android:textSize="13sp"
            android:backgroundTint="#2C2C2E"
            android:textColor="@color/text_primary" />

        <Button
            android:id="@+id/btnProfilesSheet"
            android:layout_width="wrap_content"
            android:layout_height="36dp"
            android:text="Perfiles"
            android:textSize="12sp"
            android:layout_marginStart="6dp"
            android:backgroundTint="#2C2C2E"
            android:textColor="@color/text_primary" />

        <Button
            android:id="@+id/btnFlashTop"
            android:layout_width="wrap_content"
            android:layout_height="36dp"
            android:text="⚡ Flash"
            android:textSize="12sp"
            android:layout_marginStart="6dp"
            android:backgroundTint="#F5A623"
            android:textColor="#000000" />

        <Button
            android:id="@+id/btnCreateProfileTop"
            android:layout_width="wrap_content"
            android:layout_height="36dp"
            android:text="+ Nuevo"
            android:textSize="12sp"
            android:layout_marginStart="6dp"
            android:backgroundTint="@color/accent_purple"
            android:textColor="#000000" />
    </LinearLayout>

    <FrameLayout
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1">

        <LinearLayout
            android:id="@+id/profilesScreen"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:orientation="vertical"
            android:gravity="center"
            android:padding="16dp">

            <TextView
                android:id="@+id/tvEmptyMessage"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Sin perfiles todavía"
                android:textColor="@color/text_secondary"
                android:textSize="18sp"
                android:layout_marginBottom="24dp" />

            <ScrollView
                android:id="@+id/scrollProfiles"
                android:layout_width="match_parent"
                android:layout_height="0dp"
                android:layout_weight="1"
                android:visibility="gone">
                <LinearLayout
                    android:id="@+id/llProfilesContainer"
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:orientation="vertical" />
            </ScrollView>

            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal">

                <Button
                    android:id="@+id/btnFlashSessionBig"
                    android:layout_width="0dp"
                    android:layout_height="50dp"
                    android:layout_weight="1"
                    android:text="⚡ Sesión Flash"
                    android:textColor="#000000"
                    android:textStyle="bold"
                    android:backgroundTint="#F5A623"
                    android:layout_marginEnd="6dp" />

                <Button
                    android:id="@+id/btnNewProfileBig"
                    android:layout_width="0dp"
                    android:layout_height="50dp"
                    android:layout_weight="1"
                    android:text="+ Nuevo perfil"
                    android:textColor="#000000"
                    android:textStyle="bold"
                    android:backgroundTint="@color/accent_purple" />
            </LinearLayout>
        </LinearLayout>

        <LinearLayout
            android:id="@+id/browserScreen"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:orientation="vertical"
            android:visibility="gone">

            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal"
                android:padding="8dp"
                android:background="#151515"
                android:gravity="center_vertical">

                <TextView
                    android:id="@+id/tvActiveBadge"
                    android:layout_width="0dp"
                    android:layout_height="wrap_content"
                    android:layout_weight="1"
                    android:text="Perfil Activo"
                    android:textColor="@color/accent_green"
                    android:textSize="12sp" />

                <Button
                    android:id="@+id/btnMinimize"
                    android:layout_width="wrap_content"
                    android:layout_height="32dp"
                    android:text="Minimizar"
                    android:textSize="11sp"
                    android:backgroundTint="#2C2C2E"
                    android:textColor="@color/text_primary"
                    android:layout_marginEnd="6dp" />

                <Button
                    android:id="@+id/btnClean"
                    android:layout_width="wrap_content"
                    android:layout_height="32dp"
                    android:text="Clean"
                    android:textSize="11sp"
                    android:backgroundTint="@color/accent_red"
                    android:textColor="@color/text_primary" />
            </LinearLayout>

            <FrameLayout
                android:id="@+id/webViewContainer"
                android:layout_width="match_parent"
                android:layout_height="match_parent" />
        </LinearLayout>
    </FrameLayout>
</LinearLayout>""")

with open("app/src/main/res/layout/dialog_new_profile.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:padding="20dp"
    android:background="@drawable/bg_card">

    <TextView
        android:id="@+id/tvDialogTitle"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Nuevo perfil"
        android:textColor="@color/text_primary"
        android:textSize="18sp"
        android:textStyle="bold"
        android:layout_marginBottom="14dp" />

    <EditText
        android:id="@+id/etProfileName"
        android:layout_width="match_parent"
        android:layout_height="48dp"
        android:hint="Nombre del perfil (ej. Banco PT)"
        android:textColor="@color/text_primary"
        android:textColorHint="@color/text_secondary"
        android:background="@drawable/bg_input"
        android:padding="12dp"
        android:layout_marginBottom="12dp"
        android:textSize="14sp" />

    <EditText
        android:id="@+id/etProfileUrl"
        android:layout_width="match_parent"
        android:layout_height="48dp"
        android:hint="URL del sitio (https://...)"
        android:textColor="@color/text_primary"
        android:textColorHint="@color/text_secondary"
        android:background="@drawable/bg_input"
        android:padding="12dp"
        android:textSize="14sp"
        android:inputType="textUri" />

    <TextView
        android:id="@+id/tvUrlError"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="⚠️ URL inválida (incluye http:// o https://)"
        android:textColor="@color/accent_red"
        android:textSize="12sp"
        android:paddingTop="4dp"
        android:paddingBottom="4dp"
        android:visibility="gone" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Modelo de Dispositivo:"
        android:textColor="@color/text_secondary"
        android:textSize="12sp"
        android:layout_marginTop="10dp"
        android:layout_marginBottom="4dp" />

    <Spinner
        android:id="@+id/spinnerDevices"
        android:layout_width="match_parent"
        android:layout_height="48dp"
        android:background="@drawable/bg_input"
        android:padding="8dp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Proxy (opcional):"
        android:textColor="@color/text_secondary"
        android:textSize="12sp"
        android:layout_marginTop="12dp"
        android:layout_marginBottom="4dp" />

    <LinearLayout
        android:id="@+id/btnOpenProxyDialog"
        android:layout_width="match_parent"
        android:layout_height="48dp"
        android:orientation="horizontal"
        android:background="@drawable/bg_input"
        android:padding="12dp"
        android:gravity="center_vertical"
        android:clickable="true"
        android:focusable="true">

        <TextView
            android:id="@+id/tvProxyStatusText"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="Sin proxy (Directo)"
            android:textColor="@color/text_secondary"
            android:textSize="13sp" />

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="⚙️"
            android:textSize="14sp" />
    </LinearLayout>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:layout_marginTop="18dp">

        <Button
            android:id="@+id/btnSaveOnly"
            android:layout_width="0dp"
            android:layout_height="44dp"
            android:layout_weight="1"
            android:text="Guardar perfil"
            android:textSize="12sp"
            android:backgroundTint="#2C2C2E"
            android:textColor="@color/text_primary"
            android:layout_marginEnd="6dp" />

        <Button
            android:id="@+id/btnSaveAndOpen"
            android:layout_width="0dp"
            android:layout_height="44dp"
            android:layout_weight="1"
            android:text="Guardar y abrir"
            android:textSize="12sp"
            android:backgroundTint="@color/accent_purple"
            android:textColor="#000000" />
    </LinearLayout>

    <TextView
        android:id="@+id/btnCancelDialog"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="CANCELAR"
        android:textColor="@color/text_secondary"
        android:gravity="center"
        android:padding="12dp"
        android:textSize="13sp"
        android:textStyle="bold" />
</LinearLayout>""")

with open("app/src/main/res/layout/dialog_proxy_config.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="20dp"
        android:background="@drawable/bg_card">

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Agregar proxy"
            android:textColor="@color/text_primary"
            android:textSize="18sp"
            android:textStyle="bold"
            android:layout_marginBottom="12dp" />

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Tipo de proxy"
            android:textColor="@color/text_secondary"
            android:textSize="12sp"
            android:layout_marginBottom="6dp" />

        <RadioGroup
            android:id="@+id/rgProxyType"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:layout_marginBottom="12dp">

            <RadioButton
                android:id="@+id/rbHttp"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="HTTP"
                android:textColor="@color/text_primary"
                android:textSize="12sp" />

            <RadioButton
                android:id="@+id/rbHttps"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="HTTPS"
                android:textColor="@color/text_primary"
                android:checked="true"
                android:textSize="12sp" />

            <RadioButton
                android:id="@+id/rbSocks5"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="SOCKS5"
                android:textColor="@color/text_primary"
                android:textSize="12sp" />

            <RadioButton
                android:id="@+id/rbSocks4"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="SOCKS4"
                android:textColor="@color/text_primary"
                android:textSize="12sp" />
        </RadioGroup>

        <EditText
            android:id="@+id/etProxyServer"
            android:layout_width="match_parent"
            android:layout_height="46dp"
            android:hint="Servidor (ej. 45.10.20.30)"
            android:textColor="@color/text_primary"
            android:textColorHint="@color/text_secondary"
            android:background="@drawable/bg_input"
            android:padding="12dp"
            android:layout_marginBottom="8dp"
            android:textSize="13sp" />

        <EditText
            android:id="@+id/etProxyPort"
            android:layout_width="match_parent"
            android:layout_height="46dp"
            android:hint="Puerto (ej. 8080)"
            android:textColor="@color/text_primary"
            android:textColorHint="@color/text_secondary"
            android:background="@drawable/bg_input"
            android:padding="12dp"
            android:layout_marginBottom="8dp"
            android:textSize="13sp"
            android:inputType="number" />

        <EditText
            android:id="@+id/etProxyUser"
            android:layout_width="match_parent"
            android:layout_height="46dp"
            android:hint="Usuario (opcional - Residencial)"
            android:textColor="@color/text_primary"
            android:textColorHint="@color/text_secondary"
            android:background="@drawable/bg_input"
            android:padding="12dp"
            android:layout_marginBottom="8dp"
            android:textSize="13sp" />

        <EditText
            android:id="@+id/etProxyPass"
            android:layout_width="match_parent"
            android:layout_height="46dp"
            android:hint="Contraseña (opcional)"
            android:textColor="@color/text_primary"
            android:textColorHint="@color/text_secondary"
            android:background="@drawable/bg_input"
            android:padding="12dp"
            android:layout_marginBottom="10dp"
            android:textSize="13sp"
            android:inputType="textPassword" />

        <Button
            android:id="@+id/btnTestProxy"
            android:layout_width="match_parent"
            android:layout_height="40dp"
            android:text="🧪 Probar Proxy"
            android:textSize="12sp"
            android:backgroundTint="#2C2C2E"
            android:textColor="@color/text_primary" />

        <TextView
            android:id="@+id/tvProxyTestResult"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text=""
            android:textSize="12sp"
            android:paddingTop="6dp"
            android:paddingBottom="4dp" />

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:layout_marginTop="10dp">

            <Button
                android:id="@+id/btnClearProxy"
                android:layout_width="0dp"
                android:layout_height="44dp"
                android:layout_weight="1"
                android:text="Quitar proxy"
                android:textSize="12sp"
                android:backgroundTint="#2C2C2E"
                android:textColor="@color/accent_red"
                android:layout_marginEnd="6dp" />

            <Button
                android:id="@+id/btnSaveProxy"
                android:layout_width="0dp"
                android:layout_height="44dp"
                android:layout_weight="1"
                android:text="GUARDAR"
                android:textSize="12sp"
                android:backgroundTint="@color/accent_purple"
                android:textColor="#000000" />
        </LinearLayout>

        <TextView
            android:id="@+id/btnCancelProxyDialog"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="CANCELAR"
            android:textColor="@color/text_secondary"
            android:gravity="center"
            android:padding="10dp"
            android:textSize="12sp"
            android:textStyle="bold" />
    </LinearLayout>
</ScrollView>""")

with open("app/src/main/res/layout/dialog_settings.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="20dp"
        android:background="@drawable/bg_card">

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Ajustes de API Keys (Antifraude)"
            android:textColor="@color/text_primary"
            android:textSize="18sp"
            android:textStyle="bold"
            android:layout_marginBottom="8dp" />

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Rotación automática de 6 cuentas (3 de cada una sin caché)"
            android:textColor="@color/text_secondary"
            android:textSize="12sp"
            android:layout_marginBottom="14dp" />

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Proxycheck.io Keys (1 por línea o comas):"
            android:textColor="@color/text_secondary"
            android:textSize="12sp"
            android:layout_marginBottom="4dp" />

        <EditText
            android:id="@+id/etProxycheckKeys"
            android:layout_width="match_parent"
            android:layout_height="80dp"
            android:hint="key1, key2, key3"
            android:textColor="@color/text_primary"
            android:textColorHint="@color/text_secondary"
            android:background="@drawable/bg_input"
            android:padding="10dp"
            android:gravity="top|start"
            android:layout_marginBottom="12dp"
            android:textSize="12sp" />

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Scamalytics Keys (usuario:key, 1 por línea o comas):"
            android:textColor="@color/text_secondary"
            android:textSize="12sp"
            android:layout_marginBottom="4dp" />

        <EditText
            android:id="@+id/etScamalyticsKeys"
            android:layout_width="match_parent"
            android:layout_height="80dp"
            android:hint="user1:key1, user2:key2, user3:key3"
            android:textColor="@color/text_primary"
            android:textColorHint="@color/text_secondary"
            android:background="@drawable/bg_input"
            android:padding="10dp"
            android:gravity="top|start"
            android:layout_marginBottom="14dp"
            android:textSize="12sp" />

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal">

            <Button
                android:id="@+id/btnCancelSettings"
                android:layout_width="0dp"
                android:layout_height="44dp"
                android:layout_weight="1"
                android:text="Cancelar"
                android:textSize="12sp"
                android:backgroundTint="#2C2C2E"
                android:textColor="@color/text_primary"
                android:layout_marginEnd="6dp" />

            <Button
                android:id="@+id/btnSaveSettings"
                android:layout_width="0dp"
                android:layout_height="44dp"
                android:layout_weight="1"
                android:text="Guardar claves"
                android:textSize="12sp"
                android:backgroundTint="@color/accent_purple"
                android:textColor="#000000" />
        </LinearLayout>
    </LinearLayout>
</ScrollView>""")

with open("app/src/main/res/layout/sheet_profiles.xml", "w") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:padding="16dp"
    android:background="@drawable/bg_sheet">

    <View
        android:layout_width="40dp"
        android:layout_height="4dp"
        android:background="#444444"
        android:layout_gravity="center_horizontal"
        android:layout_marginBottom="12dp" />

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:gravity="center_vertical"
        android:layout_marginBottom="12dp">

        <TextView
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="Mis Perfiles (Mosk)"
            android:textColor="@color/text_primary"
            android:textSize="18sp"
            android:textStyle="bold" />

        <Button
            android:id="@+id/btnSheetNewProfile"
            android:layout_width="wrap_content"
            android:layout_height="36dp"
            android:text="+ Nuevo"
            android:textSize="12sp"
            android:backgroundTint="@color/accent_purple"
            android:textColor="#000000" />
    </LinearLayout>

    <ScrollView
        android:layout_width="match_parent"
        android:layout_height="320dp">
        <LinearLayout
            android:id="@+id/llSheetProfiles"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical" />
    </ScrollView>
</LinearLayout>""")

with open("app/src/main/java/com/ldleo/mosk/StealthScript.kt", "w") as f:
    f.write('''package com.ldleo.mosk

object StealthScript {
    fun generate(seed: Int, vendor: String, renderer: String, userAgent: String): String {
        return """
        (function() {
            try {
                const seed = $seed;

                // 1. WebRTC Shield (Apagado completo de fugas IP)
                window.RTCPeerConnection = undefined;
                window.webkitRTCPeerConnection = undefined;

                // 2. Hardware Specs coherentes
                Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8, configurable: false });
                Object.defineProperty(navigator, 'deviceMemory', { get: () => 8, configurable: false });
                Object.defineProperty(navigator, 'maxTouchPoints', { get: () => 5, configurable: false });
                Object.defineProperty(navigator, 'platform', { get: () => 'Linux aarch64', configurable: false });

                // 3. WebGL Spoofing (Vendor y Renderer exactos)
                const fakeVendor = "$vendor";
                const fakeRenderer = "$renderer";

                function patchWebGL(proto) {
                    if (!proto) return;
                    const origGetParameter = proto.getParameter;
                    proto.getParameter = function(parameter) {
                        if (parameter === 37445) return fakeVendor;
                        if (parameter === 37446) return fakeRenderer;
                        return origGetParameter.apply(this, arguments);
                    };
                }
                patchWebGL(window.WebGLRenderingContext ? window.WebGLRenderingContext.prototype : null);
                patchWebGL(window.WebGL2RenderingContext ? window.WebGL2RenderingContext.prototype : null);

                // 4. Canvas Noise Injection (Firma matematica unica por Seed)
                const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
                HTMLCanvasElement.prototype.toDataURL = function() {
                    const ctx = this.getContext('2d');
                    if (ctx && this.width > 0 && this.height > 0) {
                        try {
                            const imgData = ctx.getImageData(0, 0, Math.min(this.width, 10), Math.min(this.height, 10));
                            for (let i = 0; i < imgData.data.length; i += 4) {
                                imgData.data[i] = (imgData.data[i] + (seed % 9) + 1) % 256;
                            }
                            ctx.putImageData(imgData, 0, 0);
                        } catch(e) {}
                    }
                    return origToDataURL.apply(this, arguments);
                };

                const origGetImageData = CanvasRenderingContext2D.prototype.getImageData;
                CanvasRenderingContext2D.prototype.getImageData = function() {
                    const res = origGetImageData.apply(this, arguments);
                    if (res && res.data && res.data.length > 0) {
                        for (let i = 0; i < Math.min(res.data.length, 60); i += 4) {
                            res.data[i] = (res.data[i] + (seed % 9) + 1) % 256;
                        }
                    }
                    return res;
                };

                // 5. AudioContext Noise Injection
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                if (AudioCtx) {
                    const origGetChannelData = AudioBuffer.prototype.getChannelData;
                    AudioBuffer.prototype.getChannelData = function(channel) {
                        const buffer = origGetChannelData.apply(this, arguments);
                        for (let i = 0; i < Math.min(buffer.length, 30); i++) {
                            buffer[i] = buffer[i] + ((seed % 7) * 0.000001);
                        }
                        return buffer;
                    };
                }

                // 6. Camouflage [native code]
                const nativeToString = Function.prototype.toString;
                const customToString = function() {
                    if (this === HTMLCanvasElement.prototype.toDataURL) {
                        return "function toDataURL() { [native code] }";
                    }
                    if (this === CanvasRenderingContext2D.prototype.getImageData) {
                        return "function getImageData() { [native code] }";
                    }
                    return nativeToString.apply(this, arguments);
                };
                Object.defineProperty(Function.prototype, 'toString', {
                    value: customToString,
                    configurable: false,
                    writable: false
                });
            } catch(e) {}
        })();
        """.trimIndent()
    }
}''')

with open("app/src/main/java/com/ldleo/mosk/ProfileModel.kt", "w") as f:
    f.write("""package com.ldleo.mosk

import org.json.JSONObject

data class DevicePreset(
    val name: String,
    val modelCode: String,
    val gpuVendor: String,
    val gpuRenderer: String,
    val userAgent: String
)

data class BrowserProfile(
    val id: String,
    var name: String,
    var startUrl: String,
    var seed: Int,
    var deviceName: String,
    var gpuVendor: String,
    var gpuRenderer: String,
    var userAgent: String,
    var proxyType: String = "DIRECT",
    var proxyHost: String = "",
    var proxyPort: Int = 0,
    var proxyUser: String = "",
    var proxyPass: String = ""
) {
    fun toJson(): JSONObject {
        val json = JSONObject()
        json.put("id", id)
        json.put("name", name)
        json.put("startUrl", startUrl)
        json.put("seed", seed)
        json.put("deviceName", deviceName)
        json.put("gpuVendor", gpuVendor)
        json.put("gpuRenderer", gpuRenderer)
        json.put("userAgent", userAgent)
        json.put("proxyType", proxyType)
        json.put("proxyHost", proxyHost)
        json.put("proxyPort", proxyPort)
        json.put("proxyUser", proxyUser)
        json.put("proxyPass", proxyPass)
        return json
    }

    companion object {
        fun fromJson(json: JSONObject): BrowserProfile {
            return BrowserProfile(
                id = json.getString("id"),
                name = json.getString("name"),
                startUrl = json.getString("startUrl"),
                seed = json.getInt("seed"),
                deviceName = json.optString("deviceName", "Samsung Galaxy S24 Ultra"),
                gpuVendor = json.getString("gpuVendor"),
                gpuRenderer = json.getString("gpuRenderer"),
                userAgent = json.optString("userAgent", "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36"),
                proxyType = json.optString("proxyType", "DIRECT"),
                proxyHost = json.optString("proxyHost", ""),
                proxyPort = json.optInt("proxyPort", 0),
                proxyUser = json.optString("proxyUser", ""),
                proxyPass = json.optString("proxyPass", "")
            )
        }

        // 6 Modelos Optimizados y Coherentes (Gama Media, Media-Alta y Alta)
        val DEVICE_CATALOG = listOf(
            DevicePreset("Samsung Galaxy S24 Ultra", "SM-S928B", "Qualcomm", "Adreno (TM) 750", "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36"),
            DevicePreset("Xiaomi POCO F6", "24069PC21G", "Qualcomm", "Adreno (TM) 735", "Mozilla/5.0 (Linux; Android 14; 24069PC21G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36"),
            DevicePreset("Google Pixel 8 Pro", "Pixel 8 Pro", "ARM", "Mali-G715", "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36"),
            DevicePreset("Samsung Galaxy S23", "SM-S911B", "Qualcomm", "Adreno (TM) 740", "Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36"),
            DevicePreset("Xiaomi 14", "23127PN0CG", "Qualcomm", "Adreno (TM) 750", "Mozilla/5.0 (Linux; Android 14; 23127PN0CG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36"),
            DevicePreset("Motorola Edge 50 Pro", "motorola edge 50 pro", "Qualcomm", "Adreno (TM) 720", "Mozilla/5.0 (Linux; Android 14; motorola edge 50 pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36")
        )
    }
}""")

with open("app/src/main/java/com/ldleo/mosk/MainActivity.kt", "w") as f:
    f.write("""package com.ldleo.mosk

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
                    ?.split(",", "\\n")?.map { it.trim() }?.filter { it.isNotEmpty() } ?: emptyList()
                val sKeys = prefs.getString("scamalytics_keys", "")
                    ?.split(",", "\\n")?.map { it.trim() }?.filter { it.isNotEmpty() } ?: emptyList()

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
                sub.text = "${p.deviceName}\n$proxyStr"
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
}""")

print("SUCCESS: All project files written cleanly!")
