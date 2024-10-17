// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME event_dict
#define R__NO_DEPRECATION

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "ROOT/RConfig.hxx"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// Header files passed as explicit arguments
#include "include/Event/uVertex.h"
#include "include/Event/uComposite.h"
#include "include/Event/uMCVertex.h"
#include "include/Event/uMCParticle.h"
#include "include/Event/uParticle.h"
#include "include/Event/TrackState.h"
#include "include/Event/uPi0.h"

// Header files passed via #pragma extra_include

// The generated code does not explicitly qualify STL entities
namespace std {} using namespace std;

namespace ROOT {
   static TClass *tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR_Dictionary();
   static void tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR_TClassManip(TClass*);
   static void *new_tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR(void *p = nullptr);
   static void *newArray_tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR(Long_t size, void *p);
   static void delete_tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR(void *p);
   static void deleteArray_tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR(void *p);
   static void destruct_tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::tuple<uPi0::Photon,uPi0::Photon>*)
   {
      ::tuple<uPi0::Photon,uPi0::Photon> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::tuple<uPi0::Photon,uPi0::Photon>));
      static ::ROOT::TGenericClassInfo 
         instance("tuple<uPi0::Photon,uPi0::Photon>", "tuple", 1232,
                  typeid(::tuple<uPi0::Photon,uPi0::Photon>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR_Dictionary, isa_proxy, 4,
                  sizeof(::tuple<uPi0::Photon,uPi0::Photon>) );
      instance.SetNew(&new_tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR);
      instance.SetNewArray(&newArray_tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR);
      instance.SetDelete(&delete_tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR);
      instance.SetDeleteArray(&deleteArray_tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR);
      instance.SetDestructor(&destruct_tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR);

      instance.AdoptAlternate(::ROOT::AddClassAlternate("tuple<uPi0::Photon,uPi0::Photon>","std::tuple<uPi0::Photon, uPi0::Photon>"));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const ::tuple<uPi0::Photon,uPi0::Photon>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const ::tuple<uPi0::Photon,uPi0::Photon>*>(nullptr))->GetClass();
      tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR_TClassManip(theClass);
   return theClass;
   }

   static void tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *TrackState_Dictionary();
   static void TrackState_TClassManip(TClass*);
   static void *new_TrackState(void *p = nullptr);
   static void *newArray_TrackState(Long_t size, void *p);
   static void delete_TrackState(void *p);
   static void deleteArray_TrackState(void *p);
   static void destruct_TrackState(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TrackState*)
   {
      ::TrackState *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::TrackState));
      static ::ROOT::TGenericClassInfo 
         instance("TrackState", "Event/TrackState.h", 7,
                  typeid(::TrackState), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &TrackState_Dictionary, isa_proxy, 4,
                  sizeof(::TrackState) );
      instance.SetNew(&new_TrackState);
      instance.SetNewArray(&newArray_TrackState);
      instance.SetDelete(&delete_TrackState);
      instance.SetDeleteArray(&deleteArray_TrackState);
      instance.SetDestructor(&destruct_TrackState);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TrackState*)
   {
      return GenerateInitInstanceLocal(static_cast<::TrackState*>(nullptr));
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const ::TrackState*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *TrackState_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const ::TrackState*>(nullptr))->GetClass();
      TrackState_TClassManip(theClass);
   return theClass;
   }

   static void TrackState_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *uParticle_Dictionary();
   static void uParticle_TClassManip(TClass*);
   static void *new_uParticle(void *p = nullptr);
   static void *newArray_uParticle(Long_t size, void *p);
   static void delete_uParticle(void *p);
   static void deleteArray_uParticle(void *p);
   static void destruct_uParticle(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::uParticle*)
   {
      ::uParticle *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::uParticle));
      static ::ROOT::TGenericClassInfo 
         instance("uParticle", "Event/uParticle.h", 12,
                  typeid(::uParticle), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &uParticle_Dictionary, isa_proxy, 4,
                  sizeof(::uParticle) );
      instance.SetNew(&new_uParticle);
      instance.SetNewArray(&newArray_uParticle);
      instance.SetDelete(&delete_uParticle);
      instance.SetDeleteArray(&deleteArray_uParticle);
      instance.SetDestructor(&destruct_uParticle);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::uParticle*)
   {
      return GenerateInitInstanceLocal(static_cast<::uParticle*>(nullptr));
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const ::uParticle*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *uParticle_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const ::uParticle*>(nullptr))->GetClass();
      uParticle_TClassManip(theClass);
   return theClass;
   }

   static void uParticle_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *uVertex_Dictionary();
   static void uVertex_TClassManip(TClass*);
   static void *new_uVertex(void *p = nullptr);
   static void *newArray_uVertex(Long_t size, void *p);
   static void delete_uVertex(void *p);
   static void deleteArray_uVertex(void *p);
   static void destruct_uVertex(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::uVertex*)
   {
      ::uVertex *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::uVertex));
      static ::ROOT::TGenericClassInfo 
         instance("uVertex", "Event/uVertex.h", 9,
                  typeid(::uVertex), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &uVertex_Dictionary, isa_proxy, 4,
                  sizeof(::uVertex) );
      instance.SetNew(&new_uVertex);
      instance.SetNewArray(&newArray_uVertex);
      instance.SetDelete(&delete_uVertex);
      instance.SetDeleteArray(&deleteArray_uVertex);
      instance.SetDestructor(&destruct_uVertex);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::uVertex*)
   {
      return GenerateInitInstanceLocal(static_cast<::uVertex*>(nullptr));
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const ::uVertex*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *uVertex_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const ::uVertex*>(nullptr))->GetClass();
      uVertex_TClassManip(theClass);
   return theClass;
   }

   static void uVertex_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *uComposite_Dictionary();
   static void uComposite_TClassManip(TClass*);
   static void *new_uComposite(void *p = nullptr);
   static void *newArray_uComposite(Long_t size, void *p);
   static void delete_uComposite(void *p);
   static void deleteArray_uComposite(void *p);
   static void destruct_uComposite(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::uComposite*)
   {
      ::uComposite *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::uComposite));
      static ::ROOT::TGenericClassInfo 
         instance("uComposite", "Event/uComposite.h", 12,
                  typeid(::uComposite), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &uComposite_Dictionary, isa_proxy, 4,
                  sizeof(::uComposite) );
      instance.SetNew(&new_uComposite);
      instance.SetNewArray(&newArray_uComposite);
      instance.SetDelete(&delete_uComposite);
      instance.SetDeleteArray(&deleteArray_uComposite);
      instance.SetDestructor(&destruct_uComposite);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::uComposite*)
   {
      return GenerateInitInstanceLocal(static_cast<::uComposite*>(nullptr));
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const ::uComposite*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *uComposite_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const ::uComposite*>(nullptr))->GetClass();
      uComposite_TClassManip(theClass);
   return theClass;
   }

   static void uComposite_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *uMCVertex_Dictionary();
   static void uMCVertex_TClassManip(TClass*);
   static void *new_uMCVertex(void *p = nullptr);
   static void *newArray_uMCVertex(Long_t size, void *p);
   static void delete_uMCVertex(void *p);
   static void deleteArray_uMCVertex(void *p);
   static void destruct_uMCVertex(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::uMCVertex*)
   {
      ::uMCVertex *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::uMCVertex));
      static ::ROOT::TGenericClassInfo 
         instance("uMCVertex", "Event/uMCVertex.h", 9,
                  typeid(::uMCVertex), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &uMCVertex_Dictionary, isa_proxy, 4,
                  sizeof(::uMCVertex) );
      instance.SetNew(&new_uMCVertex);
      instance.SetNewArray(&newArray_uMCVertex);
      instance.SetDelete(&delete_uMCVertex);
      instance.SetDeleteArray(&deleteArray_uMCVertex);
      instance.SetDestructor(&destruct_uMCVertex);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::uMCVertex*)
   {
      return GenerateInitInstanceLocal(static_cast<::uMCVertex*>(nullptr));
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const ::uMCVertex*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *uMCVertex_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const ::uMCVertex*>(nullptr))->GetClass();
      uMCVertex_TClassManip(theClass);
   return theClass;
   }

   static void uMCVertex_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *uMCParticle_Dictionary();
   static void uMCParticle_TClassManip(TClass*);
   static void *new_uMCParticle(void *p = nullptr);
   static void *newArray_uMCParticle(Long_t size, void *p);
   static void delete_uMCParticle(void *p);
   static void deleteArray_uMCParticle(void *p);
   static void destruct_uMCParticle(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::uMCParticle*)
   {
      ::uMCParticle *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::uMCParticle));
      static ::ROOT::TGenericClassInfo 
         instance("uMCParticle", "Event/uMCParticle.h", 9,
                  typeid(::uMCParticle), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &uMCParticle_Dictionary, isa_proxy, 4,
                  sizeof(::uMCParticle) );
      instance.SetNew(&new_uMCParticle);
      instance.SetNewArray(&newArray_uMCParticle);
      instance.SetDelete(&delete_uMCParticle);
      instance.SetDeleteArray(&deleteArray_uMCParticle);
      instance.SetDestructor(&destruct_uMCParticle);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::uMCParticle*)
   {
      return GenerateInitInstanceLocal(static_cast<::uMCParticle*>(nullptr));
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const ::uMCParticle*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *uMCParticle_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const ::uMCParticle*>(nullptr))->GetClass();
      uMCParticle_TClassManip(theClass);
   return theClass;
   }

   static void uMCParticle_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *uPi0_Dictionary();
   static void uPi0_TClassManip(TClass*);
   static void *new_uPi0(void *p = nullptr);
   static void *newArray_uPi0(Long_t size, void *p);
   static void delete_uPi0(void *p);
   static void deleteArray_uPi0(void *p);
   static void destruct_uPi0(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::uPi0*)
   {
      ::uPi0 *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::uPi0));
      static ::ROOT::TGenericClassInfo 
         instance("uPi0", "Event/uPi0.h", 9,
                  typeid(::uPi0), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &uPi0_Dictionary, isa_proxy, 4,
                  sizeof(::uPi0) );
      instance.SetNew(&new_uPi0);
      instance.SetNewArray(&newArray_uPi0);
      instance.SetDelete(&delete_uPi0);
      instance.SetDeleteArray(&deleteArray_uPi0);
      instance.SetDestructor(&destruct_uPi0);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::uPi0*)
   {
      return GenerateInitInstanceLocal(static_cast<::uPi0*>(nullptr));
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const ::uPi0*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *uPi0_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const ::uPi0*>(nullptr))->GetClass();
      uPi0_TClassManip(theClass);
   return theClass;
   }

   static void uPi0_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *uPi0cLcLPhoton_Dictionary();
   static void uPi0cLcLPhoton_TClassManip(TClass*);
   static void *new_uPi0cLcLPhoton(void *p = nullptr);
   static void *newArray_uPi0cLcLPhoton(Long_t size, void *p);
   static void delete_uPi0cLcLPhoton(void *p);
   static void deleteArray_uPi0cLcLPhoton(void *p);
   static void destruct_uPi0cLcLPhoton(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::uPi0::Photon*)
   {
      ::uPi0::Photon *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::uPi0::Photon));
      static ::ROOT::TGenericClassInfo 
         instance("uPi0::Photon", "Event/uPi0.h", 10,
                  typeid(::uPi0::Photon), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &uPi0cLcLPhoton_Dictionary, isa_proxy, 4,
                  sizeof(::uPi0::Photon) );
      instance.SetNew(&new_uPi0cLcLPhoton);
      instance.SetNewArray(&newArray_uPi0cLcLPhoton);
      instance.SetDelete(&delete_uPi0cLcLPhoton);
      instance.SetDeleteArray(&deleteArray_uPi0cLcLPhoton);
      instance.SetDestructor(&destruct_uPi0cLcLPhoton);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::uPi0::Photon*)
   {
      return GenerateInitInstanceLocal(static_cast<::uPi0::Photon*>(nullptr));
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const ::uPi0::Photon*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *uPi0cLcLPhoton_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const ::uPi0::Photon*>(nullptr))->GetClass();
      uPi0cLcLPhoton_TClassManip(theClass);
   return theClass;
   }

   static void uPi0cLcLPhoton_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) ::tuple<uPi0::Photon,uPi0::Photon> : new ::tuple<uPi0::Photon,uPi0::Photon>;
   }
   static void *newArray_tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) ::tuple<uPi0::Photon,uPi0::Photon>[nElements] : new ::tuple<uPi0::Photon,uPi0::Photon>[nElements];
   }
   // Wrapper around operator delete
   static void delete_tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR(void *p) {
      delete (static_cast<::tuple<uPi0::Photon,uPi0::Photon>*>(p));
   }
   static void deleteArray_tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR(void *p) {
      delete [] (static_cast<::tuple<uPi0::Photon,uPi0::Photon>*>(p));
   }
   static void destruct_tuplelEuPi0cLcLPhotoncOuPi0cLcLPhotongR(void *p) {
      typedef ::tuple<uPi0::Photon,uPi0::Photon> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class ::tuple<uPi0::Photon,uPi0::Photon>

namespace ROOT {
   // Wrappers around operator new
   static void *new_TrackState(void *p) {
      return  p ? new(p) ::TrackState : new ::TrackState;
   }
   static void *newArray_TrackState(Long_t nElements, void *p) {
      return p ? new(p) ::TrackState[nElements] : new ::TrackState[nElements];
   }
   // Wrapper around operator delete
   static void delete_TrackState(void *p) {
      delete (static_cast<::TrackState*>(p));
   }
   static void deleteArray_TrackState(void *p) {
      delete [] (static_cast<::TrackState*>(p));
   }
   static void destruct_TrackState(void *p) {
      typedef ::TrackState current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class ::TrackState

namespace ROOT {
   // Wrappers around operator new
   static void *new_uParticle(void *p) {
      return  p ? new(p) ::uParticle : new ::uParticle;
   }
   static void *newArray_uParticle(Long_t nElements, void *p) {
      return p ? new(p) ::uParticle[nElements] : new ::uParticle[nElements];
   }
   // Wrapper around operator delete
   static void delete_uParticle(void *p) {
      delete (static_cast<::uParticle*>(p));
   }
   static void deleteArray_uParticle(void *p) {
      delete [] (static_cast<::uParticle*>(p));
   }
   static void destruct_uParticle(void *p) {
      typedef ::uParticle current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class ::uParticle

namespace ROOT {
   // Wrappers around operator new
   static void *new_uVertex(void *p) {
      return  p ? new(p) ::uVertex : new ::uVertex;
   }
   static void *newArray_uVertex(Long_t nElements, void *p) {
      return p ? new(p) ::uVertex[nElements] : new ::uVertex[nElements];
   }
   // Wrapper around operator delete
   static void delete_uVertex(void *p) {
      delete (static_cast<::uVertex*>(p));
   }
   static void deleteArray_uVertex(void *p) {
      delete [] (static_cast<::uVertex*>(p));
   }
   static void destruct_uVertex(void *p) {
      typedef ::uVertex current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class ::uVertex

namespace ROOT {
   // Wrappers around operator new
   static void *new_uComposite(void *p) {
      return  p ? new(p) ::uComposite : new ::uComposite;
   }
   static void *newArray_uComposite(Long_t nElements, void *p) {
      return p ? new(p) ::uComposite[nElements] : new ::uComposite[nElements];
   }
   // Wrapper around operator delete
   static void delete_uComposite(void *p) {
      delete (static_cast<::uComposite*>(p));
   }
   static void deleteArray_uComposite(void *p) {
      delete [] (static_cast<::uComposite*>(p));
   }
   static void destruct_uComposite(void *p) {
      typedef ::uComposite current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class ::uComposite

namespace ROOT {
   // Wrappers around operator new
   static void *new_uMCVertex(void *p) {
      return  p ? new(p) ::uMCVertex : new ::uMCVertex;
   }
   static void *newArray_uMCVertex(Long_t nElements, void *p) {
      return p ? new(p) ::uMCVertex[nElements] : new ::uMCVertex[nElements];
   }
   // Wrapper around operator delete
   static void delete_uMCVertex(void *p) {
      delete (static_cast<::uMCVertex*>(p));
   }
   static void deleteArray_uMCVertex(void *p) {
      delete [] (static_cast<::uMCVertex*>(p));
   }
   static void destruct_uMCVertex(void *p) {
      typedef ::uMCVertex current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class ::uMCVertex

namespace ROOT {
   // Wrappers around operator new
   static void *new_uMCParticle(void *p) {
      return  p ? new(p) ::uMCParticle : new ::uMCParticle;
   }
   static void *newArray_uMCParticle(Long_t nElements, void *p) {
      return p ? new(p) ::uMCParticle[nElements] : new ::uMCParticle[nElements];
   }
   // Wrapper around operator delete
   static void delete_uMCParticle(void *p) {
      delete (static_cast<::uMCParticle*>(p));
   }
   static void deleteArray_uMCParticle(void *p) {
      delete [] (static_cast<::uMCParticle*>(p));
   }
   static void destruct_uMCParticle(void *p) {
      typedef ::uMCParticle current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class ::uMCParticle

namespace ROOT {
   // Wrappers around operator new
   static void *new_uPi0(void *p) {
      return  p ? new(p) ::uPi0 : new ::uPi0;
   }
   static void *newArray_uPi0(Long_t nElements, void *p) {
      return p ? new(p) ::uPi0[nElements] : new ::uPi0[nElements];
   }
   // Wrapper around operator delete
   static void delete_uPi0(void *p) {
      delete (static_cast<::uPi0*>(p));
   }
   static void deleteArray_uPi0(void *p) {
      delete [] (static_cast<::uPi0*>(p));
   }
   static void destruct_uPi0(void *p) {
      typedef ::uPi0 current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class ::uPi0

namespace ROOT {
   // Wrappers around operator new
   static void *new_uPi0cLcLPhoton(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) ::uPi0::Photon : new ::uPi0::Photon;
   }
   static void *newArray_uPi0cLcLPhoton(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) ::uPi0::Photon[nElements] : new ::uPi0::Photon[nElements];
   }
   // Wrapper around operator delete
   static void delete_uPi0cLcLPhoton(void *p) {
      delete (static_cast<::uPi0::Photon*>(p));
   }
   static void deleteArray_uPi0cLcLPhoton(void *p) {
      delete [] (static_cast<::uPi0::Photon*>(p));
   }
   static void destruct_uPi0cLcLPhoton(void *p) {
      typedef ::uPi0::Photon current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class ::uPi0::Photon

namespace ROOT {
   static TClass *vectorlEuVertexgR_Dictionary();
   static void vectorlEuVertexgR_TClassManip(TClass*);
   static void *new_vectorlEuVertexgR(void *p = nullptr);
   static void *newArray_vectorlEuVertexgR(Long_t size, void *p);
   static void delete_vectorlEuVertexgR(void *p);
   static void deleteArray_vectorlEuVertexgR(void *p);
   static void destruct_vectorlEuVertexgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<uVertex>*)
   {
      vector<uVertex> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<uVertex>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<uVertex>", -2, "vector", 423,
                  typeid(vector<uVertex>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEuVertexgR_Dictionary, isa_proxy, 4,
                  sizeof(vector<uVertex>) );
      instance.SetNew(&new_vectorlEuVertexgR);
      instance.SetNewArray(&newArray_vectorlEuVertexgR);
      instance.SetDelete(&delete_vectorlEuVertexgR);
      instance.SetDeleteArray(&deleteArray_vectorlEuVertexgR);
      instance.SetDestructor(&destruct_vectorlEuVertexgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<uVertex> >()));

      instance.AdoptAlternate(::ROOT::AddClassAlternate("vector<uVertex>","std::vector<uVertex, std::allocator<uVertex> >"));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const vector<uVertex>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEuVertexgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const vector<uVertex>*>(nullptr))->GetClass();
      vectorlEuVertexgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEuVertexgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEuVertexgR(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<uVertex> : new vector<uVertex>;
   }
   static void *newArray_vectorlEuVertexgR(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<uVertex>[nElements] : new vector<uVertex>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEuVertexgR(void *p) {
      delete (static_cast<vector<uVertex>*>(p));
   }
   static void deleteArray_vectorlEuVertexgR(void *p) {
      delete [] (static_cast<vector<uVertex>*>(p));
   }
   static void destruct_vectorlEuVertexgR(void *p) {
      typedef vector<uVertex> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class vector<uVertex>

namespace ROOT {
   static TClass *vectorlEuPi0gR_Dictionary();
   static void vectorlEuPi0gR_TClassManip(TClass*);
   static void *new_vectorlEuPi0gR(void *p = nullptr);
   static void *newArray_vectorlEuPi0gR(Long_t size, void *p);
   static void delete_vectorlEuPi0gR(void *p);
   static void deleteArray_vectorlEuPi0gR(void *p);
   static void destruct_vectorlEuPi0gR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<uPi0>*)
   {
      vector<uPi0> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<uPi0>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<uPi0>", -2, "vector", 423,
                  typeid(vector<uPi0>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEuPi0gR_Dictionary, isa_proxy, 4,
                  sizeof(vector<uPi0>) );
      instance.SetNew(&new_vectorlEuPi0gR);
      instance.SetNewArray(&newArray_vectorlEuPi0gR);
      instance.SetDelete(&delete_vectorlEuPi0gR);
      instance.SetDeleteArray(&deleteArray_vectorlEuPi0gR);
      instance.SetDestructor(&destruct_vectorlEuPi0gR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<uPi0> >()));

      instance.AdoptAlternate(::ROOT::AddClassAlternate("vector<uPi0>","std::vector<uPi0, std::allocator<uPi0> >"));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const vector<uPi0>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEuPi0gR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const vector<uPi0>*>(nullptr))->GetClass();
      vectorlEuPi0gR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEuPi0gR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEuPi0gR(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<uPi0> : new vector<uPi0>;
   }
   static void *newArray_vectorlEuPi0gR(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<uPi0>[nElements] : new vector<uPi0>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEuPi0gR(void *p) {
      delete (static_cast<vector<uPi0>*>(p));
   }
   static void deleteArray_vectorlEuPi0gR(void *p) {
      delete [] (static_cast<vector<uPi0>*>(p));
   }
   static void destruct_vectorlEuPi0gR(void *p) {
      typedef vector<uPi0> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class vector<uPi0>

namespace ROOT {
   static TClass *vectorlEuParticlegR_Dictionary();
   static void vectorlEuParticlegR_TClassManip(TClass*);
   static void *new_vectorlEuParticlegR(void *p = nullptr);
   static void *newArray_vectorlEuParticlegR(Long_t size, void *p);
   static void delete_vectorlEuParticlegR(void *p);
   static void deleteArray_vectorlEuParticlegR(void *p);
   static void destruct_vectorlEuParticlegR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<uParticle>*)
   {
      vector<uParticle> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<uParticle>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<uParticle>", -2, "vector", 423,
                  typeid(vector<uParticle>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEuParticlegR_Dictionary, isa_proxy, 4,
                  sizeof(vector<uParticle>) );
      instance.SetNew(&new_vectorlEuParticlegR);
      instance.SetNewArray(&newArray_vectorlEuParticlegR);
      instance.SetDelete(&delete_vectorlEuParticlegR);
      instance.SetDeleteArray(&deleteArray_vectorlEuParticlegR);
      instance.SetDestructor(&destruct_vectorlEuParticlegR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<uParticle> >()));

      instance.AdoptAlternate(::ROOT::AddClassAlternate("vector<uParticle>","std::vector<uParticle, std::allocator<uParticle> >"));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const vector<uParticle>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEuParticlegR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const vector<uParticle>*>(nullptr))->GetClass();
      vectorlEuParticlegR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEuParticlegR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEuParticlegR(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<uParticle> : new vector<uParticle>;
   }
   static void *newArray_vectorlEuParticlegR(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<uParticle>[nElements] : new vector<uParticle>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEuParticlegR(void *p) {
      delete (static_cast<vector<uParticle>*>(p));
   }
   static void deleteArray_vectorlEuParticlegR(void *p) {
      delete [] (static_cast<vector<uParticle>*>(p));
   }
   static void destruct_vectorlEuParticlegR(void *p) {
      typedef vector<uParticle> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class vector<uParticle>

namespace ROOT {
   static TClass *vectorlEuMCVertexgR_Dictionary();
   static void vectorlEuMCVertexgR_TClassManip(TClass*);
   static void *new_vectorlEuMCVertexgR(void *p = nullptr);
   static void *newArray_vectorlEuMCVertexgR(Long_t size, void *p);
   static void delete_vectorlEuMCVertexgR(void *p);
   static void deleteArray_vectorlEuMCVertexgR(void *p);
   static void destruct_vectorlEuMCVertexgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<uMCVertex>*)
   {
      vector<uMCVertex> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<uMCVertex>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<uMCVertex>", -2, "vector", 423,
                  typeid(vector<uMCVertex>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEuMCVertexgR_Dictionary, isa_proxy, 4,
                  sizeof(vector<uMCVertex>) );
      instance.SetNew(&new_vectorlEuMCVertexgR);
      instance.SetNewArray(&newArray_vectorlEuMCVertexgR);
      instance.SetDelete(&delete_vectorlEuMCVertexgR);
      instance.SetDeleteArray(&deleteArray_vectorlEuMCVertexgR);
      instance.SetDestructor(&destruct_vectorlEuMCVertexgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<uMCVertex> >()));

      instance.AdoptAlternate(::ROOT::AddClassAlternate("vector<uMCVertex>","std::vector<uMCVertex, std::allocator<uMCVertex> >"));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const vector<uMCVertex>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEuMCVertexgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const vector<uMCVertex>*>(nullptr))->GetClass();
      vectorlEuMCVertexgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEuMCVertexgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEuMCVertexgR(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<uMCVertex> : new vector<uMCVertex>;
   }
   static void *newArray_vectorlEuMCVertexgR(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<uMCVertex>[nElements] : new vector<uMCVertex>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEuMCVertexgR(void *p) {
      delete (static_cast<vector<uMCVertex>*>(p));
   }
   static void deleteArray_vectorlEuMCVertexgR(void *p) {
      delete [] (static_cast<vector<uMCVertex>*>(p));
   }
   static void destruct_vectorlEuMCVertexgR(void *p) {
      typedef vector<uMCVertex> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class vector<uMCVertex>

namespace ROOT {
   static TClass *vectorlEuMCParticlegR_Dictionary();
   static void vectorlEuMCParticlegR_TClassManip(TClass*);
   static void *new_vectorlEuMCParticlegR(void *p = nullptr);
   static void *newArray_vectorlEuMCParticlegR(Long_t size, void *p);
   static void delete_vectorlEuMCParticlegR(void *p);
   static void deleteArray_vectorlEuMCParticlegR(void *p);
   static void destruct_vectorlEuMCParticlegR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<uMCParticle>*)
   {
      vector<uMCParticle> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<uMCParticle>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<uMCParticle>", -2, "vector", 423,
                  typeid(vector<uMCParticle>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEuMCParticlegR_Dictionary, isa_proxy, 4,
                  sizeof(vector<uMCParticle>) );
      instance.SetNew(&new_vectorlEuMCParticlegR);
      instance.SetNewArray(&newArray_vectorlEuMCParticlegR);
      instance.SetDelete(&delete_vectorlEuMCParticlegR);
      instance.SetDeleteArray(&deleteArray_vectorlEuMCParticlegR);
      instance.SetDestructor(&destruct_vectorlEuMCParticlegR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<uMCParticle> >()));

      instance.AdoptAlternate(::ROOT::AddClassAlternate("vector<uMCParticle>","std::vector<uMCParticle, std::allocator<uMCParticle> >"));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const vector<uMCParticle>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEuMCParticlegR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const vector<uMCParticle>*>(nullptr))->GetClass();
      vectorlEuMCParticlegR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEuMCParticlegR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEuMCParticlegR(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<uMCParticle> : new vector<uMCParticle>;
   }
   static void *newArray_vectorlEuMCParticlegR(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<uMCParticle>[nElements] : new vector<uMCParticle>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEuMCParticlegR(void *p) {
      delete (static_cast<vector<uMCParticle>*>(p));
   }
   static void deleteArray_vectorlEuMCParticlegR(void *p) {
      delete [] (static_cast<vector<uMCParticle>*>(p));
   }
   static void destruct_vectorlEuMCParticlegR(void *p) {
      typedef vector<uMCParticle> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class vector<uMCParticle>

namespace ROOT {
   static TClass *vectorlEuCompositegR_Dictionary();
   static void vectorlEuCompositegR_TClassManip(TClass*);
   static void *new_vectorlEuCompositegR(void *p = nullptr);
   static void *newArray_vectorlEuCompositegR(Long_t size, void *p);
   static void delete_vectorlEuCompositegR(void *p);
   static void deleteArray_vectorlEuCompositegR(void *p);
   static void destruct_vectorlEuCompositegR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<uComposite>*)
   {
      vector<uComposite> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<uComposite>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<uComposite>", -2, "vector", 423,
                  typeid(vector<uComposite>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEuCompositegR_Dictionary, isa_proxy, 4,
                  sizeof(vector<uComposite>) );
      instance.SetNew(&new_vectorlEuCompositegR);
      instance.SetNewArray(&newArray_vectorlEuCompositegR);
      instance.SetDelete(&delete_vectorlEuCompositegR);
      instance.SetDeleteArray(&deleteArray_vectorlEuCompositegR);
      instance.SetDestructor(&destruct_vectorlEuCompositegR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<uComposite> >()));

      instance.AdoptAlternate(::ROOT::AddClassAlternate("vector<uComposite>","std::vector<uComposite, std::allocator<uComposite> >"));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const vector<uComposite>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEuCompositegR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const vector<uComposite>*>(nullptr))->GetClass();
      vectorlEuCompositegR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEuCompositegR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEuCompositegR(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<uComposite> : new vector<uComposite>;
   }
   static void *newArray_vectorlEuCompositegR(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<uComposite>[nElements] : new vector<uComposite>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEuCompositegR(void *p) {
      delete (static_cast<vector<uComposite>*>(p));
   }
   static void deleteArray_vectorlEuCompositegR(void *p) {
      delete [] (static_cast<vector<uComposite>*>(p));
   }
   static void destruct_vectorlEuCompositegR(void *p) {
      typedef vector<uComposite> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class vector<uComposite>

namespace ROOT {
   static TClass *vectorlEconstsPuParticlemUgR_Dictionary();
   static void vectorlEconstsPuParticlemUgR_TClassManip(TClass*);
   static void *new_vectorlEconstsPuParticlemUgR(void *p = nullptr);
   static void *newArray_vectorlEconstsPuParticlemUgR(Long_t size, void *p);
   static void delete_vectorlEconstsPuParticlemUgR(void *p);
   static void deleteArray_vectorlEconstsPuParticlemUgR(void *p);
   static void destruct_vectorlEconstsPuParticlemUgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<const uParticle*>*)
   {
      vector<const uParticle*> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<const uParticle*>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<const uParticle*>", -2, "vector", 423,
                  typeid(vector<const uParticle*>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEconstsPuParticlemUgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<const uParticle*>) );
      instance.SetNew(&new_vectorlEconstsPuParticlemUgR);
      instance.SetNewArray(&newArray_vectorlEconstsPuParticlemUgR);
      instance.SetDelete(&delete_vectorlEconstsPuParticlemUgR);
      instance.SetDeleteArray(&deleteArray_vectorlEconstsPuParticlemUgR);
      instance.SetDestructor(&destruct_vectorlEconstsPuParticlemUgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<const uParticle*> >()));

      instance.AdoptAlternate(::ROOT::AddClassAlternate("vector<const uParticle*>","std::vector<uParticle const*, std::allocator<uParticle const*> >"));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const vector<const uParticle*>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEconstsPuParticlemUgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const vector<const uParticle*>*>(nullptr))->GetClass();
      vectorlEconstsPuParticlemUgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEconstsPuParticlemUgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEconstsPuParticlemUgR(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<const uParticle*> : new vector<const uParticle*>;
   }
   static void *newArray_vectorlEconstsPuParticlemUgR(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<const uParticle*>[nElements] : new vector<const uParticle*>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEconstsPuParticlemUgR(void *p) {
      delete (static_cast<vector<const uParticle*>*>(p));
   }
   static void deleteArray_vectorlEconstsPuParticlemUgR(void *p) {
      delete [] (static_cast<vector<const uParticle*>*>(p));
   }
   static void destruct_vectorlEconstsPuParticlemUgR(void *p) {
      typedef vector<const uParticle*> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class vector<const uParticle*>

namespace ROOT {
   static TClass *vectorlETrackStategR_Dictionary();
   static void vectorlETrackStategR_TClassManip(TClass*);
   static void *new_vectorlETrackStategR(void *p = nullptr);
   static void *newArray_vectorlETrackStategR(Long_t size, void *p);
   static void delete_vectorlETrackStategR(void *p);
   static void deleteArray_vectorlETrackStategR(void *p);
   static void destruct_vectorlETrackStategR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<TrackState>*)
   {
      vector<TrackState> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<TrackState>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<TrackState>", -2, "vector", 423,
                  typeid(vector<TrackState>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlETrackStategR_Dictionary, isa_proxy, 4,
                  sizeof(vector<TrackState>) );
      instance.SetNew(&new_vectorlETrackStategR);
      instance.SetNewArray(&newArray_vectorlETrackStategR);
      instance.SetDelete(&delete_vectorlETrackStategR);
      instance.SetDeleteArray(&deleteArray_vectorlETrackStategR);
      instance.SetDestructor(&destruct_vectorlETrackStategR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<TrackState> >()));

      instance.AdoptAlternate(::ROOT::AddClassAlternate("vector<TrackState>","std::vector<TrackState, std::allocator<TrackState> >"));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const vector<TrackState>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlETrackStategR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const vector<TrackState>*>(nullptr))->GetClass();
      vectorlETrackStategR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlETrackStategR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlETrackStategR(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<TrackState> : new vector<TrackState>;
   }
   static void *newArray_vectorlETrackStategR(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<TrackState>[nElements] : new vector<TrackState>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlETrackStategR(void *p) {
      delete (static_cast<vector<TrackState>*>(p));
   }
   static void deleteArray_vectorlETrackStategR(void *p) {
      delete [] (static_cast<vector<TrackState>*>(p));
   }
   static void destruct_vectorlETrackStategR(void *p) {
      typedef vector<TrackState> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class vector<TrackState>

namespace {
  void TriggerDictionaryInitialization_libEvent_Impl() {
    static const char* headers[] = {
"include/Event/uVertex.h",
"include/Event/uComposite.h",
"include/Event/uMCVertex.h",
"include/Event/uMCParticle.h",
"include/Event/uParticle.h",
"include/Event/TrackState.h",
"include/Event/uPi0.h",
nullptr
    };
    static const char* includePaths[] = {
"/disk/homedisk/home/user294/Documents/selections",
"/disk/homedisk/home/user294/Documents/selections/include/",
"/cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc12-opt/include",
"/disk/homedisk/home/user294/Documents/selections/include/",
"/cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc12-opt/include",
"/cvmfs/sft.cern.ch/lcg/releases/ROOT/6.30.02-fb5be/x86_64-el9-gcc12-opt/include/",
"/disk/homedisk/home/user294/Documents/selections/build/",
nullptr
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "libEvent dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_AutoLoading_Map;
struct __attribute__((annotate("$clingAutoload$Event/uParticle.h")))  __attribute__((annotate("$clingAutoload$include/Event/uVertex.h")))  uParticle;
namespace std{template <typename _Tp> class __attribute__((annotate("$clingAutoload$bits/allocator.h")))  __attribute__((annotate("$clingAutoload$string")))  allocator;
}
struct __attribute__((annotate("$clingAutoload$include/Event/uVertex.h")))  uVertex;
struct __attribute__((annotate("$clingAutoload$include/Event/uComposite.h")))  uComposite;
struct __attribute__((annotate("$clingAutoload$include/Event/uPi0.h")))  uPi0;
struct __attribute__((annotate("$clingAutoload$include/Event/uMCVertex.h")))  uMCVertex;
struct __attribute__((annotate("$clingAutoload$include/Event/uMCParticle.h")))  uMCParticle;
struct __attribute__((annotate("$clingAutoload$Event/TrackState.h")))  __attribute__((annotate("$clingAutoload$include/Event/uVertex.h")))  TrackState;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "libEvent dictionary payload"

#ifndef RECO4D
  #define RECO4D 0
#endif

#define _BACKWARD_BACKWARD_WARNING_H
// Inline headers
#include "include/Event/uVertex.h"
#include "include/Event/uComposite.h"
#include "include/Event/uMCVertex.h"
#include "include/Event/uMCParticle.h"
#include "include/Event/uParticle.h"
#include "include/Event/TrackState.h"
#include "include/Event/uPi0.h"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[] = {
"TrackState", payloadCode, "@",
"uComposite", payloadCode, "@",
"uMCParticle", payloadCode, "@",
"uMCVertex", payloadCode, "@",
"uParticle", payloadCode, "@",
"uPi0", payloadCode, "@",
"uPi0::Photon", payloadCode, "@",
"uVertex", payloadCode, "@",
nullptr
};
    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("libEvent",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_libEvent_Impl, {}, classesHeaders, /*hasCxxModule*/false);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_libEvent_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_libEvent() {
  TriggerDictionaryInitialization_libEvent_Impl();
}
