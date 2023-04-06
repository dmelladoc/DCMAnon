# Anonimizador de DICOM

Script para borrar metadatos especificos de un DICOM para su anonimizacion

Los campos anonimizados son los siguientes:

* (8, 34) AcquisitionDate
* (8, 129) InstitutionAddress
* (8, 144) ReferringPhysicianName
* (8, 4176) PerformingPhysicianName
* (16, 16) PatientName
* (16, 32) PatientID
* (16, 48) PatientBirthDate
* (16, 64) PatientSex
* (16, 4096) OtherPatientIDs
* (16, 4112) PatientAge
* (16, 4144) PatientWeight
* (16, 8192) MedicalAlerts
* (16, 8464) Allergies
* (16, 8544) EthnicGroup
* (16, 8576) Occupation
* (16, 8624) AdditionalPatientHistory
* (16, 8640) PregnancyStatus
* (56, 768) CurrentPatientLocation


## requisitos
* pydicom
* pandas
* tqdm 

## Ejecucion

```sh
python dicom_anonimize.py [ruta carpetas] -o out/
```