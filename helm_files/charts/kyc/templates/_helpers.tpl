{{- define "kyc.FULL_NAME" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}


{{- define "kyc.IMAGE" -}}
{{- .Values.global.KYC_IMAGE -}}
{{- end -}}