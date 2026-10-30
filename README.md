> Пути ниже указаны от `src/main/java/ru/urfu/platform/`, номера строк даны по этой копии.

---

# Часть 1 StPlatform

## 1. Слои: что есть в проекте

Контроллеры HTML:
- `web/AssignmentPageController`, 
- `web/CabinetController`, 
- `web/TeacherAssignmentController`, 
- `web/TeacherStudentController`, 
- `web/TeacherImportController`, 
- `web/AttachmentController`, 
- `web/LoginController`, 
- `web/ActivateController`, 
- `web/PasswordResetController`, 
- `consent/ConsentPageController`

Контроллеры REST:
- `api/ApiSubmissionController`, 
- `api/ApiAssignmentController`, 
- `api/ApiAuthController`

Сервисы:
- `submission/SubmissionService`, 
- `assigment/AssignmentService`, 
- `user/UserService`, 
- `consent/ConsentService`, 
- `auth/ActivationService`, 
- `auth/PasswordResetService`, 
- `student/StudentRemovalService`, 
- `security/PlatformUserDetailsService`

Репозитории:
- `submission/SubmissionRepository`, 
- `submission/SubmissionAttachmentRepository`, 
- `assigment/AssignmentRepository`, 
- `user/UserRepository`, 
- `consent/ConsentRecordRepository`

Ни один контроллер не импортирует JPA-репозиторий. `ApiAuthController` держит только `SecurityContextRepository` из Spring Security, это не слой хранения.

## 2. Трассировка: «сдать домашку»

`POST /assignments/{id}/submit` (форма студента на странице задания)

```
web/AssignmentPageController.submitWork
 ├→ user/UserService.byId
 │    └→ UserRepository.findById
 ├→ AssignmentPageController.splitLinks (private)
 └→ submission/SubmissionService.submit
      ├→ AssignmentRepository.findById
      ├→ SubmissionService.ensureNotAlreadySent
      │    └→ SubmissionRepository.findFirstByStudentIdAndAssignmentIdOrderByCreatedAtDesc
      ├→ Assignment.deadlinePassed()
      ├→ LinkValidator.isValid
      ├→ SubmissionRepository.save
      ├→ AttachmentStorage.store(file)
      └→ SubmissionAttachmentRepository.save
 ← Submission
AssignmentPageController: flash «Работа принята на проверку» → redirect:/assignments/{id} (PRG)
```

Короткая форма цепочки:
`AssignmentPageController.submitWork → SubmissionService.submit → SubmissionRepository.save → БД`

Ошибки идут обратно вверх исключениями. `BadRequestException` и `ForbiddenException` контроллер ловит и показывает flash-сообщением, 
`NotFoundException` превращает в ответ `WebExceptionHandler`. Нижние слои HTTP-кодов не знают.

Тот же сценарий есть в REST: `api/ApiSubmissionController.submit` (:72) вызывает тот же `SubmissionService.submit(..., file = null)`.

## 3. Все ли стрелки идут вниз?

В основном да. Контроллер → сервис → репозиторий → БД. Репозитории не импортируют ничего из `web/`/`api/`. `common/` ни от кого не зависит. 
Удаление студента вынесено в отдельный пакет `student/StudentRemovalService`.

## 4. Где провёл бы границу иначе

- Файл в сервис передавать как свою абстракцию, а не как `MultipartFile`. Контроллер превращает `MultipartFile` 
в record `UploadedFile(name, contentType, size, InputStream)`. Сервис и хранилище после этого от Spring Web не зависят, 
а REST, бот или импорт смогут передавать файл тем же методом.
- `AttachmentStorage` спрятать за интерфейсом `FileStorage`. Сейчас репозитории уже интерфейсы, а хранилище файлов остаётся конкретным классом. 
- Все веб-классы собрать в `web/`. Туда переезжают `BlockedUserInterceptor`, `ConsentInterceptor` и `ConsentPageController`. 
Цикл `user ↔ security` исчезает, в доменных пакетах не остаётся servlet-импортов.

## 5. Зачем эта граница (одной фразой)

Граница Controller | Service нужна, чтобы правила сдачи (дедлайн, запрет повторной сдачи, лимиты ссылок, проверка файла) жили 
в одном `SubmissionService` и не зависели от того, кто их вызывает: HTML-форма, REST API или будущий бот. 
Поэтому `SubmissionServiceTest` проверяет их на Mockito-заглушках, без HTTP и без БД.

---

# PetClinic: «добавление визита» через агента

**Агент:** субагент `general-purpose` в Claude, запущенный из этой сессии. Он сам клонировал `spring-projects/spring-petclinic` (ветка `main`, коммит `500158f` от 2026-09-29) и прочитал код.
**Модель агента:** Claude Sonnet 5.5 (`claude-sonnet-5-5`).
**Сверка:** основная сессия на Claude Opus 5.5 (`claude-opus-5-5`) открыла `VisitController`, `Owner` и `Pet` и проверила, что номера строк и цепочка совпадают с кодом. Ошибок агента не нашлось.

Пути ниже указаны от `src/main/java/org/springframework/samples/petclinic/`.

## Слои

- **Controller:** `owner/OwnerController`, `PetController`, `VisitController`, `vet/VetController`, `system/WelcomeController`, `CrashController`.
- **Service:** **нет**. В `src/main/java` нет ни одного `@Service`.
- **Repository:** `owner/OwnerRepository`, `PetTypeRepository` (`JpaRepository`), `vet/VetRepository`.
- **Entity:** `Owner`, `Pet`, `Visit`, `PetType`, `Vet`, `Specialty`. Базовые классы в `model/`: `BaseEntity`, `NamedEntity`, `Person`.

## Цепочка: GET-форма → POST-сохранение

```
GET  /owners/{ownerId}/pets/{petId}/visits/new
VisitController.loadPetWithVisit  (@ModelAttribute, :63)  — срабатывает ДО хендлера
  → OwnerRepository.findById(ownerId)  :66                → БД (owner + pets + visits, EAGER)
  → Owner.getPet(petId)  :70  →  new Visit()  →  Pet.addVisit(visit)  :79
→ VisitController.initNewVisitForm  :91                   → "pets/createOrUpdateVisitForm"

POST /owners/{ownerId}/pets/{petId}/visits/new
VisitController.loadPetWithVisit  :63  (снова: findById → getPet → new Visit)
→ биндинг формы + @Valid Visit (description @NotBlank)
→ VisitController.processNewVisitForm  :98
    проверка «дата строго в будущем»  :100   (правило — в контроллере)
  → Owner.addVisit(petId, visit)  :108  → Pet.addVisit  (Owner.java:176)
  → OwnerRepository.save(owner)  :109   → БД: INSERT visits  (каскад Owner → Pet → Visit, cascade = ALL)
  → redirect:/owners/{ownerId}  :111   (PRG + flash «Your visit has been booked»)
```

Короткая форма: `VisitController.processNewVisitForm → Owner.addVisit → OwnerRepository.save → БД`