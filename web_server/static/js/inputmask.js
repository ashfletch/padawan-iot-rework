function applyInputMask() {
  $('.ip_address').mask('099.099.099.099');
  $('.mac_address').mask('ZZ:ZZ:ZZ:ZZ:ZZ:ZZ', {
    translation: {
      'Z': {
        pattern: /[A-Fa-f0-9]/,
        optional: false
      }
    }
  })
}