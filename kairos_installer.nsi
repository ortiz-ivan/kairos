; NSIS Installer Script para Kairos
; Requiere: NSIS (https://nsis.sourceforge.io)

!include "MUI2.nsh"

; ============================================
; Configuración Básica
; ============================================
Name "Kairos 1.0"
OutFile "KairosInstaller.exe"
InstallDir "$PROGRAMFILES\Kairos"
InstallDirRegKey HKCU "Software\Kairos" ""

; Mostrar licencia
LicenseData "LICENSE.txt"

; ============================================
; Interfaz MUI
; ============================================
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "Spanish"

; ============================================
; Secciones de Instalación
; ============================================
Section "Instalar Kairos"
    SetOutPath "$INSTDIR"

    ; Copiar el ejecutable y archivos
    File /r "dist\Kairos.exe"
    File /r "dist\*.*"

    ; Crear shortcuts
    CreateDirectory "$SMPROGRAMS\Kairos"
    CreateShortcut "$SMPROGRAMS\Kairos\Kairos.lnk" "$INSTDIR\Kairos.exe"
    CreateShortcut "$SMPROGRAMS\Kairos\Desinstalar.lnk" "$INSTDIR\Uninstall.exe"

    ; Crear shortcut en escritorio
    CreateShortcut "$DESKTOP\Kairos.lnk" "$INSTDIR\Kairos.exe"

    ; Guardar ruta de instalación
    WriteRegStr HKCU "Software\Kairos" "" $INSTDIR

    ; Crear desinstalador
    WriteUninstaller "$INSTDIR\Uninstall.exe"

    ; Agregar a "Agregar o quitar programas"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Kairos" "DisplayName" "Kairos"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Kairos" "UninstallString" "$INSTDIR\Uninstall.exe"

SectionEnd

; ============================================
; Sección de Desinstalación
; ============================================
Section "Desinstalar"
    RMDir /r "$INSTDIR"
    RMDir /r "$SMPROGRAMS\Kairos"
    Delete "$DESKTOP\Kairos.lnk"
    DeleteRegKey HKCU "Software\Kairos"
    DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Kairos"
SectionEnd
