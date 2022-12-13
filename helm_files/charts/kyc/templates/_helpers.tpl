{{- define "kyc.FULL_NAME" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}


{{- define "kyc.IMAGE" -}}
{{- .Values.global.KYC_IMAGE -}}
{{- end -}}

{{- define "kyc.FLAGSMITH_API_KEY" -}}
{{- .Values.global.FLAGSMITH_API_KEY -}}
{{- end -}}


{{- define "kyc.DATABASE_URL" -}}
{{- .Values.global.DATABASE_URL -}}
{{- end -}}
